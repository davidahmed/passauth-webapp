from pymongo import MongoClient

class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient('mongodb://dave123:awesomeGuy@localhost:27017')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()