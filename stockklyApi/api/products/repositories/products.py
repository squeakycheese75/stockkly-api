# from stockklyApi.api import auth
from stockklyApi.database.db import get_db
import json
from bson import json_util
# from bson.objectid import ObjectId


def get_product(ticker):
    db = get_db()['stockkly']
    product_collection = db['products']

    queryresult = product_collection.find_one({"ticker": ticker.upper()})

    return queryresult


def get_products():
    db = get_db()['stockkly']
    product_collection = db['products']

    queryresult = product_collection.find({})
    json_results = json_util.dumps(queryresult)
    return json_results

    # return json_util.dumps({'success': True, 'products': queryresult})


def create_product(data):
    db = get_db()['stockkly']
    product_collection = db['products']

    queryresult = product_collection.find_one({"ticker": data['ticker'].upper()})

    if not queryresult:
        product = {
            "ticker": data['ticker'].upper(),
            "displayTicker":  data['displayTicker'],
            "name": data['name'],
            "description": data['description'],
            "company": data['company'],
            "sector": data['sector'],
            "quote": data['quote'],
            "exchange": data['exchange']
        }
        product_collection.insert_one(product)
    return


def upsert_product(data, ticker):
    db = get_db()['stockkly']
    product_collection = db['products']

    product = {
        "ticker": data['ticker'].upper(),
        "displayTicker":  data['displayTicker'],
        "name": data['name'],
        "description": data['description'],
        "company": data['company'],
        "sector": data['sector'],
        "quote": data['quote'],
        "exchange": data['exchange']
    }
    return product_collection.update_one({'ticker': ticker.upper()}, {"$set": product}, upsert=True)
