import json


def test_process_valid_receipt(app, sample_receipt_data):
    """Test processing a valid receipt."""
    response = app.post('/receipts/process', json=sample_receipt_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "id" in data


def test_process_invalid_receipt(app):
    """Test processing an invalid receipt."""
    invalid_data = {
        "retailer": "Target",  # Missing other fields
    }
    response = app.post('/receipts/process', json=invalid_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

# Add more comprehensive tests for various scenarios:
# 1. Receipt with invalid retailer format.
# 2. Receipt with invalid purchaseDate format.
# 3. Receipt with invalid purchaseTime format.
# 4. Receipt with items missing required fields.
# 5. Receipt with invalid total format.

# Add test for the /receipts/{id}/points endpoint after is implemented.
