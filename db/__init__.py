''' This module interacts with the database

NOTE: database and port in app_resources/config.py

Functions:
- insert_one adds data and optionally a comment into the specified collection
'''

from site import addsitedir
addsitedir("../")

from app_resources.config import MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_DATABASE_NAME

import pymongo

def create_connection(collection: str = "default") -> pymongo.collection.Collection: 
    '''Takes in the name of the collection and connects using configurations from app_resources/config.py'''
    try:
        return pymongo.collection.Collection(
            pymongo.database.Database(
                pymongo.MongoClient(f"mongodb://{ MONGO_DB_HOST }:{ MONGO_DB_PORT }/"), MONGO_DB_DATABASE_NAME
                ),
            collection
            )
    except Exception as e:
        message = f'''Error finding Database at {MONGO_DB_HOST}:{MONGO_DB_PORT} called {MONGO_DB_DATABASE_NAME}
{e}
'''
        raise ValueError(message)            

def insert_one(data, collection: str = "default", comment: str = "") -> None:
    '''Inserts 'data' into the collection named 'collection' with an optional comment, returning the id'''

    connect = create_connection(collection)
    result = connect.insert_one(data, comment=comment)
    connect.database.client.close()

    try:
        return result.inserted_id
    except Exception as e:
        message = f'''Error while inserting data ({data}) and comment "{comment}" into collection "{collection}"
into a Database at {MONGO_DB_HOST}:{MONGO_DB_PORT} called {MONGO_DB_DATABASE_NAME}
{e}
'''
        raise ValueError(message)
    

__all__ =["insert_one"]