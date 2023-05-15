import sys
import re

from flask import Flask, jsonify, request
from pymongo import MongoClient
from helpers.methods import (
    toStrings,
    sanitizeName,
    sanitizePageAndLimit,
    convert_to_dict,
)

# from flask_cors import CORS
import os

port = int(os.environ.get("PORT", 5000))


sys.path.append("/helpers")


app = Flask(__name__)
# CORS(app)
app.config.from_pyfile("config.py")


try:
    client = MongoClient(app.config["DATABASE_URI"])
    db = client[app.config["DATABASE_NAME"]]

    collection = db[app.config["COLLECTION_NAME"]]
    # creating indexes will increase the overhead
    # in this case the search has is as fast with as without the indexes
    # using indexes when we rely on text should be faster when working with large datasets
    # collection.create_index([("product_title", "text")])
except Exception as e:
    raise Exception("Error connecting to the database: ", e)


# Route to search for data by name
@app.route("/api/data/search", methods=["POST"])
def search_data():
    # Get the name and page number from the request body
    name = request.json.get("name")
    page = request.json.get("page", 1)
    limit = request.json.get("limit", 10)

    # Sanitize the name parameter
    name = sanitizeName(name)
    if not name:
        return (
            jsonify(
                {
                    "data": [],
                    "total_count": 0,
                    "total_pages": 1,
                    "current_page": 1,
                    "limit": limit,
                }
            ),
            200,
        )

    # Sanitize and validate the page and limit parameters
    page, limit = sanitizePageAndLimit(page, limit)

    data = (
        collection.find({"product_title": {"$regex": re.compile(name, re.IGNORECASE)}})
        .skip((page - 1) * limit)
        .limit(limit)
    )

    # Convert the data to a list of dictionaries
    data = convert_to_dict(data)

    # If there is no data, return an error response
    if not data:
        return (
            jsonify(
                {
                    "data": [],
                    "total_count": 0,
                    "total_pages": 1,
                    "current_page": 1,
                    "limit": limit,
                }
            ),
            200,
        )

    # Convert the ObjectId to a string
    data = toStrings(data)
    if not data:
        return (
            jsonify(
                {
                    "data": [],
                    "total_count": 0,
                    "total_pages": 1,
                    "current_page": 1,
                    "limit": limit,
                }
            ),
            200,
        )

    # Count the total number of documents that match the search criteria
    total_count = collection.count_documents(
        {"product_title": {"$regex": re.compile(name, re.IGNORECASE)}}
    )
    # Calculate the total number of pages based on the limit parameter
    total_pages = (total_count + limit - 1) // limit

    # Return the data and pagination information as a JSON response
    return jsonify(
        {
            "data": data,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "limit": limit,
        }
    )


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
# flake8: noqa
