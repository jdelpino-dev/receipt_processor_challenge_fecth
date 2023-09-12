import pytest
from receipts import Receipt
from marshmallow import ValidationError


def test_receipt_validation(sample_receipt_data, invalid_receipt_data):
    # Test each sample receipt data for validity
    for data in sample_receipt_data:
        receipt = Receipt(data)
        assert receipt is not None

    # Test each invalid receipt data for errors
    for data in invalid_receipt_data:
        with pytest.raises(ValidationError):
            Receipt(data)


def test_generate_id(sample_receipt_data):
    # Test that each receipt gets a unique ID
    ids = set()
    for data in sample_receipt_data:
        receipt = Receipt(data)
        assert receipt.id is not None
        assert len(str(receipt.id)) == 36  # UUIDs are 36 characters long
        assert receipt.id not in ids
        ids.add(receipt.id)


def test_points_calculation(sample_receipt_data):
    expected_points = [12, 109, 28]

    for data, points in zip(sample_receipt_data, expected_points):
        receipt = Receipt(data)
        assert receipt.points == points


def test_add_receipt_to_pool(
        receipt_pool,
        sample_receipt_data,
        list_of_receipt_ids
):
    # This test will check if the receipts are added to the pool
    for data in sample_receipt_data:
        receipt = Receipt(data)
        receipt_pool.add_receipt(receipt)
        assert receipt.id in receipt_pool.data
        list_of_receipt_ids.append(receipt.id)


def test_get_receipt_from_pool(receipt_pool, list_of_receipt_ids):
    # Test retrieval of receipts
    for id in list_of_receipt_ids:
        receipt = receipt_pool.get_receipt(id)
        assert receipt is not None


def test_delete_receipt_from_pool(filled_receipt_pool, sample_receipt_data):
    # Test deletion of receipts
    for data in sample_receipt_data:
        receipt = Receipt(data)
        filled_receipt_pool.delete_receipt(receipt.id)
        assert receipt.id not in filled_receipt_pool.data
