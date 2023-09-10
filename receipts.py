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
            self.id = self._generate_id()
            self.points = self._calculate_points()
            self.data = receipt
