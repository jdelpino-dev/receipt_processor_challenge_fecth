import pytest
from receipts import Receipt, Receipt_Pool
from marshmallow import ValidationError


def test_receipt_validation():
    # Test a valid receipt
    valid_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }
    receipt = Receipt(valid_data)
    assert receipt is not None

    # Test an invalid receipt
    invalid_data = {
        # Missing retailer
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }
    with pytest.raises(ValidationError):
        Receipt(invalid_data)


def test_generate_id():
    valid_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }
    receipt = Receipt(valid_data)
    assert receipt.id is not None
    assert len(str(receipt.id)) == 36  # UUIDs are 36 characters long


def test_points_calculation():
    valid_data = {
        "retailer": "Target1",  # 7 alphanumeric chars
        "purchaseDate": "2022-01-02",  # Odd day: +6 points
        "purchaseTime": "15:01",  # After 2 PM but before 4 PM: +10 points
        "items": [
            # Not multiple of 3
            {"price": "6.49", "shortDescription": "Mountain Dew 12PK"}
        ],
        "total": "6.49"  # Not 0 cents, not multiple of 0.25
    }
    receipt = Receipt(valid_data)
    expected_points = 7 + 6 + 10
    assert receipt.points == expected_points


def test_add_receipt_to_pool():
    pool = Receipt_Pool()
    valid_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }
    receipt = Receipt(valid_data)
    pool.add_receipt(receipt)
    assert receipt.id in pool.data


def test_get_receipt_from_pool():
    pool = Receipt_Pool()
    valid_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }
    receipt = Receipt(valid_data)
    pool.add_receipt(receipt)
    retrieved_receipt = pool.get_receipt(receipt.id)
    assert retrieved_receipt.id == receipt.id


def test_delete_receipt_from_pool():
    pool = Receipt_Pool()
    valid_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }
    receipt = Receipt(valid_data)
    pool.add_receipt(receipt)
    pool.delete_receipt(receipt.id)
    assert receipt.id not in pool.data
