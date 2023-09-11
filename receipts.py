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
        raise NotImplementedError


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

    def get_receipt(self, receipt_id: UUID) -> Receipt:
        return self.data[receipt_id]

    def get_all_receipts(self) -> Dict[UUID, Receipt]:
        return self.data

    def delete_receipt(self, receipt_id: UUID):
        del self.data[receipt_id]


# Validations Schemas for the Receipt class using marshmallow. The schemas
# are base in the regex patterns provided in challenge OpenAPI specification.


class ItemSchema(Schema):
    shortDescription = fields.Str(
        required=True, validate=validate.Regexp(r"^[\\w\\s\\-]+$"))
    price = fields.Str(
        required=True, validate=validate.Regexp(r"^\\d+\\.\\d{2}$"))


class ReceiptSchema(Schema):
    retailer = fields.Str(required=True, validate=validate.Regexp(r"^\\S+$"))
    purchaseDate = fields.Date(required=True, format="%Y-%m-%d")
    purchaseTime = fields.Time(required=True, format="%H:%M")
    items = fields.List(fields.Nested(ItemSchema),
                        required=True, validate=validate.Length(min=1))
    total = fields.Str(
        required=True, validate=validate.Regexp(r"^\\d+\\.\\d{2}$"))
