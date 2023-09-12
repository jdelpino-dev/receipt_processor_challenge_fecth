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
# Flask imports
from flask import Flask, request
# Classes for the Receipt and Receipt_Pool
from receipts import Receipt, Receipt_Pool
# Marshmallow for data validation of the request payload
from marshmallow import ValidationError
# Logging imports
import logging
from logging.handlers import RotatingFileHandler


# Initialize and config the Flask application
app = Flask(__name__)

# Initialize the Receipt_Pool object to store the receipts
receipt_pool = Receipt_Pool()

# Set up logging

# Create an alias for the Flask app logger
app_logger = app.logger

# Configure the logging settings to determine how logs should be handled.
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_file = 'logs/app.log'  # Define the path to the log file

# Create a rotating file handler to handle the logs in development
log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=3)

# Set up the log handler and add it to the Flask app
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)
app_logger.addHandler(log_handler)

# Initializaton log message
app_logger.info('Receipt Processor API started successfully.')

# API routes

# Monitor/Log the types of requests your server is receiving


@app.before_request
def log_request_info():
    app_logger.debug('Headers: %s', request.headers)
    app_logger.info('Body: %s', request.get_data())


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
        app_logger.info(f"Processed receipt with ID: {receipt.id}")

        # Add the receipt to the receipt pool
        receipt_pool.add_receipt(receipt)

        # Return the receipt id as a response
        return {"id": receipt.id}, 200

    except ValidationError as error:
        # If there's a validation error, log it, return the error message
        # and a 400 status code
        app_logger.warning(f"Validation error occurred: {error}")
        return {"error": str(error)}, 400

    except Exception:
        # Log the detailed error for debugging
        app_logger.exception("An unexpected error occurred.")
        return (
            {"error": "An error occurred processing the receipt."},
            500
        )


@app.teardown_appcontext
def cleanup(error=None):
    if error:
        app_logger.error(f"Error during shutdown: {error}")

    # app_logger.info(
    #     "Application context is being torn down."
    #     "Cleanup operations go here."
    # )
    app_logger.info("Application/Request context ended.")
