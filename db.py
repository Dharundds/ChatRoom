from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import User

client = MongoClient(
    "mongodb+srv://Centigrade:Centigrade@centigrade-chatroom.l4cxo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

chat_db = client.get_database("ChatDB")
users_collections = chat_db.get_collection("users")


def save_user(username, password):
    password = generate_password_hash(password)
    users_collections.insert_one({'_id': username, 'password': password})


def get_user(username):
    user_data = users_collections.find_one({'_id': username})
    return User(user_data['_id'], user_data['password']) if user_data else None


if __name__ == "__main__":
    save_user("zaid", "zaid")
