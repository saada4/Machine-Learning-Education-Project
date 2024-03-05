''' This module interacts with the database

NOTE: database and port in app_resources/config.py

Functions:
- insert_one adds a "document" (json convertible) and optionally a comment into the specified collection
- insert_many adds "documents" (iterable of json convertibles) and optionally a comment into the specified collection
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

def insert_one(document, collection: str = "default", comment: str = "") -> None:
    '''Inserts 'document' into the collection named 'collection' with an optional comment, returning the id'''

    connect = create_connection(collection)
    result = connect.insert_one(document, comment=comment)
    connect.database.client.close()

    try:
        return result.inserted_id
    except Exception as e:
        message = f'''Error while inserting data ({document}) and comment "{comment}" into collection "{collection}"
into a Database at {MONGO_DB_HOST}:{MONGO_DB_PORT} called {MONGO_DB_DATABASE_NAME}
{e}
'''
        raise ValueError(message)
    
def insert_many(documents, collection: str = "default", comment: str = "") -> list:
    """Inserts from iterable 'documents' into the collection named 'collection' with an optional comment, returning the id's in order"""

    connect = create_connection(collection)
    result = connect.insert_many(documents, comment=comment)
    connect.database.client.close()

    try:
        return result.inserted_ids
    except Exception as e:
        message = f'''Error while inserting data ({documents}) and comment "{comment}" into collection "{collection}"
into a Database at {MONGO_DB_HOST}:{MONGO_DB_PORT} called {MONGO_DB_DATABASE_NAME}
{e}
'''
        raise ValueError(message)
    

__all__ =["insert_one", "insert_many"]