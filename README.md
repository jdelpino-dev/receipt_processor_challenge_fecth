# Receipt Processor API and Microservice

### Fetch Rewards Backend Engineering Apprenticeship Coding Exercise

**Solution by:** José Delpino [delpinoivivas@gmail.com](mailto:delpinoivivas@gmail.com)

**September 2023**

**Written in** Python 3.11.5 and Flask 2.3.3

---

## Table of Contents

- [Introduction](#introduction)
- [Design Context](#design-context)
- [Retailer Name Problem](#retailer-name-problem)
- [Dockerizing the Receipt Processor API](#dockerizing-the-receipt-processor-api)
- [Test Suite](#test-suite)
- [Future Improvements for Scalability and Production](#future-improvements-for-scalability-and-production)
- [API Endpoints](#api-endpoints)
- [Point Calculation Rules](#point-calculation-rules)
- [Self Evaluation](#self-evaluation)
- [Examples](#examples)

---

## Introduction

The Receipt Processor API is designed to handle the processing of receipts and award points based on specific criteria. This document provides a detailed explanation of the solution, its design considerations, and potential improvements.

## Design Context

### Assumptions

- This API, along with its encompassing microservice, will be better integrated into a broader application or system comprised of multiple microservices.
- Each microservice autonomously manages its in-memory and/or database storage and other operations, choosing the most fitting data storage solution tailored to its specific needs.
- In the future, multiple instances of this microservice will operate concurrently for scalability.

### Focus

- The primary focus has been on designing the API and the Receipt class, as well as unit tests, data validation, error handling, and foundational error logging.

- The Receipt class currently processes and stores receipts in memory. It is envisioned that this class will eventually handle persistent database storage of receipts and other scalability-driven operations.

- Using a class-based approach to represent a receipt allows for easier integration with other classes and functions in the future. For example, a separate Point Calculator class could be introduced to manage more dynamic and complex point calculation rules.

---

## Retailer Name Problem

In the original challenge's OpenAPI specification, the regex pattern for the retailer's name did not allow for spaces. This omission was a potential oversight since real-world retailer names often contain spaces. The revised pattern allows names with spaces but prevents names with leading or trailing spaces. This adjustment ensures that the API can handle real-world retailer names while maintaining data integrity.

---

## Dockerizing the Receipt Processor API

### Building the Docker Container

To build a Docker container for the Receipt Processor API, navigate to the project's root directory and run:

```bash
docker build -t receipt-processor:latest .
```

### Running the App (by default it runs in debug mode)

Once the Docker image is built, you can run the Flask app with:

```bash
docker run -p 5000:5000 receipt-processor:latest
```

This command runs the app in debug mode. The app should now be accessible at `http://localhost:5000`.

#### Port Troubleshooting

If you have trouble running the app or accessing the API, please ensure that port 5000 is not in use by another process. You can try changing the port mapping in the `docker run` command to a different port (e.g., `-p 5001:5000`), and so on. Common ports that could be available are 5000-5008, 5500-5509, 8000-8008, and 8080-8088.

#### Permissions Troubleshooting

Sometimes the docker commands need to be run in sudo mode, if you have problems running the commands try to run them with sudo.

### Running the App in regular Mode

If don't want to run the app in debug mode you must use a different command to run the app. this command will override the original command in the Dockerfile and will run the app in regular mode.

```bash
docker run -p 5001:5000 -e FLASK_APP=app.py receipt-processor:latest flask run --host=0.0.0.0
```

#### Port Troubleshooting

All the port troubleshooting mentioned above applies to this command as well.

### Running the Tests in the Docker Container

To run the unit tests inside the Docker container, use:

```bash
docker run receipt-processor:latest python -m pytest -v
```

This command will execute all the tests and display the results.

---

## Test Suite

- The code is tested using `pytest` and it's currently passing all tests.

- I recommend to run the tests using the following command:

```bash
`python -m pytest -v'
```

Or this in case your usgin docker:

```bash
docker run receipt-processor:latest python -m pytest -v
```

- The current test suite is not comprehensive and does not include end-to-end tests. The current tests are meant to serve as a foundation for future tests.

- While the current tests cover a significant portion of the functionality, there are always more edge cases and scenarios that can be tested. Additional tests could be added to cover more nuanced scenarios or integrations.

- Tests related to the `Receipt` class validation rely on the `marshmallow` library's `ValidationError`. It's essential to ensure that the schema in the `Receipt` class remains updated and in sync with the expected data structure.

---

## Future Improvements for Scalability and Production

1. **Database Integration**: While the current solution uses in-memory storage for receipts, integrating a relational database (like PostgreSQL) would allow for persistent storage and more efficient data retrieval operations.

2. **Authentication and Authorization**: Implementing token-based authentication (like JWT) would secure the API endpoints, ensuring that only authorized users can access and manipulate data.

3. **Rate Limiting**: Incorporating rate limiting can prevent potential misuse of the API, ensuring that a single user or bot cannot overwhelm the service with requests.

4. **Logging Enhancements**: Enhancing logging to include more detailed request and response logs, errors, and system events would provide better insights into application behavior and assist in debugging. Also is necessary handle the logs in a centralized location and also manage them
   diferently when tessting.

5. **Horizontal Scalability**: Considering containerization (e.g., using Docker) and orchestration tools (like Kubernetes) would allow the application to scale horizontally, handling a larger number of concurrent users.

6. **Redis Caching**: Using Redis as a caching layer would allow for faster data retrieval and better performance.

---

## API Endpoints

### Process Receipts

- **Path**: `/receipts/process`
- **Method**: `POST`
- **Payload**: Receipt JSON
- **Response**: JSON containing an ID for the receipt.

This endpoint takes a JSON receipt, processes it, calculates the points based on specified rules, and returns a unique ID for the receipt.

### Get Points

- **Path**: `/receipts/{id}/points`
- **Method**: `GET`
- **Response**: A JSON object containing the number of points awarded.

This endpoint retrieves the points awarded for a specific receipt using its unique ID.

---

## Point Calculation Rules

- One point for every alphanumeric character in the retailer name.
- 50 points if the total is a round dollar amount with no cents.
- 25 points if the total is a multiple of `0.25`.
- 5 points for every two items on the receipt.
- If the trimmed length of the item description is a multiple of 3, multiply the price by `0.2` and round up to the nearest integer to get the points earned.
- 6 points if the day in the purchase date is odd.
- 10 points if the time of purchase is after 2:00 pm and before 4:00 pm.

---

## Self Evaluation

- This solution was built with extensibility, scalability, and real-world applicability in mind.

- Most of the code is well-documented and follows PEP-8 guidelines. The code is also tested for unit tests and and simple integration/functional tests.

- While not fully production-ready, it serves as a foundation upon which additional features and optimizations can be built.

For further queries or clarifications, feel free to reach out to José Delpino
at [delpinoivivas@gmail.com](mailto:delpinoivivas@gmail.com)

---

## Examples

```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },
    {
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },
    {
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },
    {
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },
    {
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
```

```text
Total Points: 28
Breakdown:
     6 points - retailer name has 6 characters
    10 points - 4 items (2 pairs @ 5 points each)
     3 Points - "Emils Cheese Pizza" is 18 characters (a multiple of 3)
                item price of 12.25 * 0.2 = 2.45, rounded up is 3 points
     3 Points - "Klarbrunn 12-PK 12 FL OZ" is 24 characters (a multiple of 3)
                item price of 12.00 * 0.2 = 2.4, rounded up is 3 points
     6 points - purchase day is odd
  + ---------
  = 28 points
```

---

```json
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
```

```text
Total Points: 109
Breakdown:
    50 points - total is a round dollar amount
    25 points - total is a multiple of 0.25
    14 points - retailer name (M&M Corner Market) has 14 alphanumeric characters
                note: '&' is not alphanumeric
    10 points - 2:33pm is between 2:00pm and 4:00pm
    10 points - 4 items (2 pairs @ 5 points each)
  + ---------
  = 109 points
```
