from .db import MongoDBConnection

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
    pass

def get_user_logs(username):
    pass

