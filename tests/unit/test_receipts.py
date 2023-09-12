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
    expected_points = [17, 109, 28]

    for data, points in zip(sample_receipt_data, expected_points):
        receipt = Receipt(data)
        assert receipt.points == points


def test_add_receipt_to_pool(filled_receipt_pool, sample_receipt_data):
    # This test will check that all sample receipts are indeed in the pool
    for data in sample_receipt_data:
        receipt = Receipt(data)
        assert receipt.id in filled_receipt_pool.data


def test_get_receipt_from_pool(filled_receipt_pool, sample_receipt_data):
    # Test retrieval of receipts
    for data in sample_receipt_data:
        receipt = Receipt(data)
        retrieved_receipt = filled_receipt_pool.get_receipt(receipt.id)
        assert retrieved_receipt.id == receipt.id


def test_delete_receipt_from_pool(filled_receipt_pool, sample_receipt_data):
    # Test deletion of receipts
    for data in sample_receipt_data:
        receipt = Receipt(data)
        filled_receipt_pool.delete_receipt(receipt.id)
        assert receipt.id not in filled_receipt_pool.data
