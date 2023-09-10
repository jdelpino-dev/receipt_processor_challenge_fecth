"""
Receipt Processor API
Fetch Rewards Backend Engineerin Apprenticeship Coding Exercise
Solution by: José Delpino
September 2023

Written in Python 3.11.5 and Flask 2.3.3
"""

from flask import Flask, request, jsonify
from receipts import Receipt

app = Flask(__name__)


# API routes

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    # Get the request data and transforming it into a dictionary
    receipt_data = request.get_json()

    # Process the receipt: it will assing it an unique id,
    # calculate the points it was awarded, and store it in memory.
    receipt = Receipt(receipt_data)

    # Returning the receipt id as a response
    # return jsonify(receipt.id)
    return jsonify({"id": receipt.id})
