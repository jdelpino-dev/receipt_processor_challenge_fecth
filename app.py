"""
------------------------------------------------------------------------
Receipt Processor API - Main Application
Fetch Rewards Backend Engineering Apprenticeship Coding Exercise
Solution by: José Delpino (delpinoivivas@gmail.com)
September 2023

------------------------------------------------------------------------

Written in Python 3.11.5 and Flask 2.3.3

------------------------------------------------------------------------
"""

from flask import Flask, request
from receipts import Receipt, Receipt_Pool
from marshmallow import ValidationError

# Initialize the Flask application and the Receipt_Pool in memory
app = Flask(__name__)
receipt_pool = Receipt_Pool()


# API routes

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    # Get the request data and transforming it into a dictionary
    receipt_data = request.get_json()

    # Validate the receipt data from the request payload
    # and process the receipt
    try:
        # Process the receipt: it will assing it an unique id,
        # calculate the points it was awarded, and store it in memory.
        receipt = Receipt(receipt_data)

        # Return the receipt id as a response
        return {"id": receipt.id}, 200

    except ValidationError as error:
        # If there's a validation error, return the error message
        # and a 400 status code
        return {"error": str(error)}, 400

    except Exception as error:
        # Handle other unforeseen errors
        return (
            {"error": f"An error occurred processing the receipt: {error}."},
            500
        )
