import hashlib
from .db import MongoDBConnection

commonUsernames = ['admin']

def user_md5(username):
    return hashlib.md5(username.encode('utf-8')).hexdigest()

def validate_signup(username, password):
    if len(username) < 5:
        return False, "Invalid Username!"
    if username in commonUsernames:
        return False, "Username is too common. Maybe be a bit special today?"
        return False,
    if len(password) < 8:
        return False, "Invalid Password!"
    if not any(char.isdigit() for char in password):
        return False, "Did you forget to use numbers in your password?"
    if not any(char.isalpha() for char in password):
        return False, "Invalid Password!"
    return True, ""


def user_exists(username):
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection['passauth']
        if db.users.find_one({'u': username}):
            print(db.users.find_one({'u': username}))
            return True
        return False


def authenticate(username, password):
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection['passauth']
        if db.users.find_one({'u': username, 'p': password}):
            print(db.users.find_one({'u': username}))
            return True
        return False

def register_user(username, password):
    mongo = MongoDBConnection()

    with mongo:
        assert user_exists(username) == False, "Fatal: Registering an existing user"
        db = mongo.connection['passauth']
        result = db.users.insert_one({
            'u': username,
            'p': password,
            'sessions': 0
        })
        print('User added {0}'.format(result.inserted_id))
        return True

def get_user_session(username, increment=False):
    mongo = MongoDBConnection()

    with mongo:
        assert user_exists(username) == True, "Fatal: User doesn't even exist"
        db = mongo.connection['passauth']
        if increment:
            db.users.update({'u': username}, { '$inc': {'sessions':1}})
        return db.users.find_one({'u': username}).get('sessions',False)

def put_user_logs(username, logs):
    mongo = MongoDBConnection()

    with mongo:
        assert user_exists(username), "Fatal: User doesn't even exist"
        db_collection = mongo.connection['passauth'][user_md5(username)]
        print(logs)
        #logs.pop('rawData', None)
        return db_collection.insert_one(logs).acknowledged

def get_user_logs(username):
    pass

