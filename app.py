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

While tackling this challenge, I made the following assumptions:

[1] This API along with its encompassing microservice will be better integrated
into a broader application or system comprised of multiple microservices.

[2] Each microservice autonomously manages its in-memory and/or database
storage and other operations. Furthermore, each microservice selects
the most fitting data storage solution tailored to its specific needs.

[3] In the future, multiple instances of this microservice will operate
concurrently for scalability.

At this stage, my primary focus has been on designing the API and
the Receipt class, as well as unit tests, data validation, error handling,
and foundational error logging.

The Receipt class is currently responsible for processing and storing
receipts in memory. Moving forward, it's envisaged that this class will
extend its capabilities to handle persistent database storage of receipts
and other advanced scalability-driven operations.

Using a class to represent a receipt will also allow for easier integration
with other classes and functions in the future. For example,
a point calculator class could be created to handle more dynamic
and complex rules. This dynamic rules could be fetched from a database
or data source shared with other microservices.


------------------------------------------------------------------------
"""

from flask import Flask, request
from receipts import Receipt, Receipt_Pool

# Initialize the Flask application and the Receipt_Pool in memory
app = Flask(__name__)
receipt_pool = Receipt_Pool()


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
    return {"id": receipt.id}
