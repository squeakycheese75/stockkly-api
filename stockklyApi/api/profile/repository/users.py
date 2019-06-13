from stockklyApi.database.db import get_db


def get_user(userId):
    db = get_db()['stockkly']
    user_collection = db['users']

    queryresult = user_collection.find_one({"userId": userId.lower()})
    return queryresult


def create_user(data, userId):
    db = get_db()['stockkly']
    user_collection = db['users']

    queryresult = user_collection.find_one({"userId": userId.lower()})

    if not queryresult:
        user = {
            "userId": userId.lower(),
            "watchList": data['watchList'],
            "currency": data['currency'],
            "symbol": data['symbol'],
            "refreshRate": data['refreshRate']
        }
        user_collection.insert_one(user)
    return


def upsert_user(data, userId):
    db = get_db()['stockkly']
    user_collection = db['users']

    user = {
        "watchList": data['watchList'],
        "currency": data['currency'],
        "symbol": data['symbol'],
        "refreshRate": data['refreshRate']
    }
    return user_collection.update_one({'userId': userId.lower()}, {"$set": user}, upsert=True)