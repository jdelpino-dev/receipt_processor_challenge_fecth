"""
------------------------------------------------------------------------
Receipt Processor API — Main Application
Fetch Rewards Backend Engineering Apprenticeship Coding Exercise
Solution by: José Delpino (delpinoivivas@gmail.com)
September 2023

------------------------------------------------------------------------

Written in Python 3.11.5 and Flask 2.3.3

------------------------------------------------------------------------

Design Context

While addressing this challenge, I operated under the assumption that both
this API and its encompassing microservice will eventually integrate into
a broader application or system comprised of multiple microservices.
Each microservice, I assume, autonomously manages its in-memory and/or
database storage, along with other operations. Moreover, it's anticipated
that in the future, multiple instances of this microservice will operate
concurrently for scalability.

At this stage, my primary focus has been on designing the API and
the Receipt class, as well as unittests, data validation, error handling,
and basic error logging.

The Receipt class is currently responsible for processing and storing
receipts in memory. Moving forward, it's envisaged that this class will
extend its capabilities to handle persistent database storage of receipts
and other advanced scalability-driven operations.

------------------------------------------------------------------------
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
