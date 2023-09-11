"""
Receipt Processor API – Receipt Class

Fetch Rewards Backend Engineering Apprenticeship Coding Exercise
Solution by: José Delpino
September 2023

Written in Python 3.11.5 and Flask 2.3.3
"""
from typing import Dict
import uuid  # Python standard library for generating unique ids


class Receipt:
    """
    A class to represent a receipt. It will be used to store the receipt data,
    assign it an unique id, calculate the points awarded, and store
    the receipt in memory.

    It will handle the future storage of the receipts in a database
    and other future operations.
    """

    def __init__(self, receipt: dict):
        if self.validate_receipt(receipt):
            self.id: uuid.UUID = self.generate_id()
            self.points: int = self.calculate_points()
            self.data: dict = receipt

    def validate_receipt(self, receipt: dict) -> bool:
        """
        Validates the receipt data using marshmallow.
        """
        raise NotImplementedError

    def generate_id(self) -> uuid.UUID:
        """
        Generates an unique id for the receipt using uuid4, which
        is based on random numbers and has a very low probability
        of collision.
        """
        return uuid.uuid4()

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
        self.data: Dict[uuid.UUID, Receipt] = {}

    def add_receipt(self, receipt: Receipt):
        # Safety check to avoid id collisions
        while receipt.id in self.data:
            receipt.id = receipt.generate_id()

        self.data[receipt.id] = receipt

    def get_receipt(self, receipt_id: uuid.UUID) -> Receipt:
        return self.data[receipt_id]

    def get_all_receipts(self) -> Dict[uuid.UUID, Receipt]:
        return self.data

    def delete_receipt(self, receipt_id: uuid.UUID):
        del self.data[receipt_id]
