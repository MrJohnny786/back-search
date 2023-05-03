from bson import ObjectId
import re


def toStrings(data):
    if data:
        for document in data:
            # Check if the document has an _id field and if it's an ObjectId
            if "_id" in document and isinstance(document["_id"], ObjectId):
                # Convert the ObjectId to a string
                document["_id"] = str(document["_id"])
        return data
    else:
        return None


def sanitizeName(name):
    if name:
        name = re.sub(r"[^\w\s-]", "", name)
        if name:
            return name
        else:
            return None
    else:
        return None


def sanitizePageAndLimit(page=1, limit=10):
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        page = 1
        limit = 10
    if page < 1:
        page = 1
    if limit < 1 or limit > 1000:
        limit = 10

    return page, limit


def convert_to_dict(data):
    # Convert the data to a list of dictionaries
    data = [document for document in data]
    return data
