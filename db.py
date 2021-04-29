from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import User

client = MongoClient(
    "mongodb+srv://Centigrade:Centigrade@centigrade-chatroom.l4cxo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

chat_db = client.get_database("ChatDB")
users_collections = chat_db.get_collection("users")
room_collections = chat_db.get_collection("room")
messages_collections = chat_db.get_collection("messages")
room_members_collections = chat_db.get_collection("room_members")


def save_user(username, password, email_address):
    password = generate_password_hash(password)
    users_collections.insert_one(
        {'_id': username, 'password': password, 'email_address': email_address})


def get_user(username):
    user_data = users_collections.find_one({'_id': username})
    return User(user_data['_id'], user_data['password']) if user_data else None


def check_user(username):
    user = users_collections.find_one({'_id': username})
    return user if user else None


def save_room(room_name, created_by):
    room_id = room_collections.insert_one(
        {'name': room_name, 'created_by': created_by, 'created_at': datetime.now()}).inserted_id
    add_room_member(room_id, room_name, created_by, created_by, is_admin=True)
    return room_id


def update_room(room_id, room_name):
    room_collections.update_one({'_id': ObjectId(room_id)}, {
                                '$set': {'name': room_name}})
    room_members_collections.update_many({'_id.room_id': ObjectId(room_id)}, {
                                         '$set': {'room_name': room_name}})


def get_room(room_id):
    return room_collections.find_one({'_id': ObjectId(room_id)})


def add_room_member(room_id, room_name, username, added_by, is_admin=False):
    room_members_collections.insert_one({
        '_id': {'room_id': room_id, 'username': username},
        'room_name': room_name,
        'added_by': added_by,
        'added_at': datetime.now(),
        'is_room_admin': is_admin
    })


def add_room_members(room_id, room_name, usernames, added_by):
    # since many users are added list of dictionary is added
    room_members_collections.insert_many([{
        '_id': {'room_id': ObjectId(room_id), 'username': username},
        'room_name': room_name,
        'added_by': added_by,
        'added_at': datetime.now(),
        'is_room_admin': False} for username in usernames])


def update_admin(room_id, username):
    if username:
        room_members_collections.update_many({
            '_id': {'room_id': ObjectId(room_id), 'username': username}}, {'$set': {'is_room_admin': True}}
        )
    else:
        pass


def remove_admin(room_id, username):
    if username:
        room_members_collections.update_one({
            '_id': {'room_id': ObjectId(room_id), 'username': username}}, {'$set': {'is_room_admin': False}}
        )
    else:
        pass


def remove_room_members(room_id, usernames):
    # $in multiple  values that can be taken by _id
    room_members_collections.delete_many(
        {'_id': {'$in': [{'room_id': room_id, 'username': username} for username in usernames]}})


def remove_room_member(room_id, username):
    room_members_collections.delete_one({
        '_id': {
            'room_id': ObjectId(room_id),
            'username': username
        }
    })


def get_room_members(room_id):
    return list(room_members_collections.find({'_id.room_id': ObjectId(room_id)}))


def get_rooms_for_user(username):
    return list(room_members_collections.find({'_id.username': username}))


def is_room_member(room_id, username):
    return room_members_collections.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}})


def is_room_admin(room_id, username):
    return room_members_collections.count_documents({'_id': {'room_id': ObjectId(
        room_id), 'username': username}, 'is_room_admin': True})


def save_msg(room_id, text, sender):
    messages_collections.insert_one(
        {'room_id': room_id, 'text': text, 'sender': sender, 'created_at': datetime.now()})


def get_messages(room_id):

    messages = list(messages_collections.find({'room_id': room_id}))
    for message in messages:
        message['created_at'] = message['created_at'].strftime('%d %b, %H:%M')

    return messages


def get_email(username):
    try:
        email = users_collections.find_one({'_id': username})
        return email['email_address'] if email else None
    except:
        email = "no email"
        return email


def delete_room(room_id):
    rooms_collections.delete_one({'_id': ObjectId(room_id)})
