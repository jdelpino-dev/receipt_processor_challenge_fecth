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
import logging
from logging.handlers import RotatingFileHandler


# Initialize the Flask application and the Receipt_Pool in memory
app = Flask(__name__)
receipt_pool = Receipt_Pool()

# Set up logging

# Configure the logging settings to determine how logs should be handled.
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_file = 'logs/app.log'  # Define the path to the log file

# Create a rotating file handler to handle the logs in development
log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=3)

# Set up the log handler and add it to the Flask app
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)

# Initializaton log message
app.logger.info('Receipt Processor API started successfully.')

# API routes

# Monitor/Log the types of requests your server is receiving


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())


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

        # Logs the if og the processed receipt
        app.logger.info(f"Processed receipt with ID: {receipt.id}")

        # Return the receipt id as a response
        return {"id": receipt.id}, 200

    except ValidationError as error:
        # If there's a validation error, log it, return the error message
        # and a 400 status code
        app.logger.warning(f"Validation error occurred: {error}")
        return {"error": str(error)}, 400

    except Exception:
        # Log the detailed error for debugging
        app.logger.exception("An unexpected error occurred.")
        return (
            {"error": "An error occurred processing the receipt."},
            500
        )


@app.teardown_appcontext
def cleanup(error=None):
    if error:
        app.logger.error(f"Error during shutdown: {error}")

    # app.logger.info(
    #     "Application context is being torn down."
    #     "Cleanup operations go here."
    # )

    app.logger.info("Application/Request context ended.")
