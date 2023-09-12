"""
Receipt Processor API - Receipt Class

Fetch Rewards Backend Engineering Apprenticeship Coding Exercise
Solution by: José Delpino
September 2023

Written in Python 3.11.5 and Flask 2.3.3
"""
from typing import Dict
from uuid import UUID, uuid4  # From Python standard library for unique ids
from marshmallow import Schema, fields, validate, ValidationError


class Receipt:
    """
    A class to represent a receipt. It will be used to store the receipt data,
    assign it an unique id, calculate the points awarded, and store
    the receipt in memory.

    It will handle the future storage of the receipts in a database
    and other future operations.
    """

    def __init__(self, receipt: dict):
        # Attempt to validate the receipt. If validation fails,
        # the ValidationError exception will be raised and can be caught
        # outside this method in the specific route.
        self.validate_receipt(receipt)

        self.id: UUID = self.generate_id()
        self.points: int = self.calculate_points()
        self.data: dict = receipt

    def validate_receipt(self, receipt: dict) -> bool:
        """ Use Marshmallow schema to validate the receipt data """
        schema = ReceiptSchema()
        errors = schema.validate(receipt)
        if errors:
            # If there are validation errors, raise an exception including
            # the detail errors
            raise ValidationError(f"Receipt validation failed: {errors}")

    def generate_id(self) -> UUID:
        """
        Generates an unique id for the receipt using uuid4, which
        is based on random numbers and has a very low probability
        of collision.
        """
        return uuid4()

    def calculate_points(self) -> int:
        """
        Calculates the points awarded for the receipt. It currently
        uses hardcoded rules, but it will be extended to use
        dynamic rules in the future. It will possible be refacttored
        into a separate class: Points_Calculator.
        """
        points = 0

        # One point for every alphanumeric character in the retailer's name
        points += count_alphanumeric(self.data["retailer"])

        # 50 points if the total is round dollar amount with no cents
        if has_zero_cents(self.data["total"]):
            points += 50

        # 25 points if the total is multiple of 0.25
        if float(self.data["total"]) % 0.25 == 0:
            points += 25

        # 5 points for every two items on the receipt
        points += len(self.data["items"]) // 2 * 5

        # If the trimmed lenght of the item description is a multiple of 3,
        # multiply the price by 0.2 and round up to the nearest integer.
        for item in self.data["items"]:
            if len(item["shortDescription"].strip()) % 3 == 0:
                points += round(float(item["price"]) * 0.2)

        # 6 points if the day in the purchase date is odd
        if get_day(self.data["purchaseDate"]) % 2 == 1:
            points += 6

        # 10 points if the time of the purchase is after 2:00 PM (14:00)
        # and before 4:00 PM (16:00)
        hour, minute = split_time(self.data["purchaseTime"])
        if hour == 15 or (hour == 14 and minute > 0):
            points += 10

        return points


class Receipt_Pool:
    """
    A class to represent the receipt pool. It will be used to store
    the receipts in memory.
    """

    def __init__(self):
        self.data: Dict[UUID, Receipt] = {}

    def add_receipt(self, receipt: Receipt):
        # Safety check to avoid id collisions
        while receipt.id in self.data:
            receipt.id = receipt.generate_id()

        self.data[receipt.id] = receipt
        app_logger = get_logger()
        app_logger.info(f"Added receipt with ID {receipt.id} to the pool.")

    def get_receipt(self, receipt_id: UUID) -> Receipt:
        return self.data.get(receipt_id, None)

    def get_all_receipts(self) -> Dict[UUID, Receipt]:
        return self.data

    def delete_receipt(self, receipt_id: UUID) -> bool:
        app_logger = get_logger()
        if self.data.get(receipt_id, None):
            del self.data[receipt_id]
            app_logger.info(
                f"Deleted receipt with ID {receipt_id} from the pool.")
            return True

        else:
            app_logger.warning(
                f"Attempted to delete receipt with ID {receipt_id}, but it was not found in the pool.")
            return False


# Validations Schemas for the Receipt class using marshmallow. The schemas
# are base in the regex patterns provided in challenge OpenAPI specification.


# Schema for individual items on a receipt.
class ItemSchema(Schema):
    # Validates that the short description contains only alphanumeric
    # characters, spaces, and hyphens. Accepts descriptions with trailing and
    # leading spaces.
    shortDescription = fields.Str(
        required=True, validate=validate.Regexp(r"^[\w\s\-]+$"))
    # Validates that the price is in the format of digits, followed by
    # a period, and then exactly two digits.
    price = fields.Str(
        required=True, validate=validate.Regexp(r"^\d+\.\d{2}$"))


# Schema for the receipt itself
class ReceiptSchema(Schema):
    # Validates that the retailer's name contains only non-space characters.
    retailer = fields.Str(required=True, validate=validate.Regexp(r"^\S+$"))
    purchaseDate = fields.Date(required=True, format="%Y-%m-%d")
    # Validates if the input is in a 24-hour format like HH:MM
    purchaseTime = fields.Time(
        required=True,
        format="%H:%M",
        validate=validate.Regexp(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    )
    # Validates that there's at least one item in the receipt.
    items = fields.List(fields.Nested(ItemSchema),
                        required=True, validate=validate.Length(min=1))
    # Similar to the item price, this validates that the total is
    # in the correct monetary format.
    total = fields.Str(
        required=True, validate=validate.Regexp(r"^\d+\.\d{2}$"))


# Module helper functions

def get_logger():
    """Lazily import the app logger to avoid circular imports"""
    from app import app_logger
    return app_logger


def has_zero_cents(price_str: str) -> bool:
    _, cents = price_str.split(".")
    return cents == "00"


def count_alphanumeric(s):
    """Count the number of alphanumeric characters in a string"""
    return sum(1 for char in s if char.isalnum())


def get_day(date_str: str) -> int:
    """Get the day from a date string in the format YYYY-MM-DD"""
    return int(date_str.split("-")[2])


def split_time(time_str: str) -> tuple:
    time_list = time_str.split(":")
    hour = time_list[0]
    minutes = time_list[1]
    return hour, minutes
