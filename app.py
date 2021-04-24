from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send
from db import (add_room_members, get_messages, get_user, save_msg, save_room,
                save_user, get_rooms_for_user, get_room, is_room_member,
                get_room_members, is_room_admin, update_room, remove_room_members, update_admin, remove_admin, add_room_member, remove_room_member)
from datetime import datetime
from bson.json_util import dumps


app = Flask(__name__)
app.secret_key = 'Centigrade'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    rooms = []
    have_rooms = False

    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
        a = len(rooms)
        if a == 0:
            have_rooms = False
        else:
            have_rooms = True
    return render_template('index.html', rooms=rooms, have_rooms=have_rooms)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    message = 'ㅤ'
    if request.method == "POST":
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home', username=current_user.username))
        else:
            message = 'Failed to login'

    return render_template('login.html', message=message)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    message = ''
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email_address = request.form.get('email_address')
        user = get_user(username)
        message = 'ㅤ'
        if user:
            message = 'User already exist'
        else:
            save_user(username, password, email_address)

            return redirect(url_for('home'))

    return render_template('signup.html', message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/', methods=["GET", "POST"])
@login_required
def create_room():
    message = ''
    if request.method == "POST":
        room_name = request.form.get('room_name')
        usernames = [username.strip()
                     for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames,
                             current_user.username)
            return redirect(url_for('chat_room', room_id=room_id))
        else:
            message = 'Failed to Create room'

    return render_template('index.html', message1=message)


@app.route('/rooms/<room_id>/edit', methods=["POST", "GET"])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    admins = []
    not_admin = []
    if room and is_room_admin(room_id, current_user.username):
        message = ''
        members = get_room_members(room_id)
        for member in members:
            if is_room_admin(room_id, member['_id']['username']):
                admins.append(member['_id']['username'])
            else:
                not_admin.append(member['_id']['username'])
        if request.method == "POST":
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)
            make_admin = request.form.get('makeAdmin')
            removeAdmin = request.form.get('removeAdmin')
            add_member = request.form.get('addmember')
            rem_mem = request.form.get('remove_user')


            if make_admin:
                print(make_admin)
                update_admin(room_id, make_admin)
            if removeAdmin:
                remove_admin(room_id, removeAdmin)
            try:
                if add_member:
                    add_mems = [username.strip()
                                for username in add_member.split(',')]
                    add_room_members(room_id, room_name, add_mems,
                                    current_user.username)
            except:
                print("bruhhh")                        
            if rem_mem:
                print('hi')
                print(room_id, rem_mem)
                remove_room_member(room_id, rem_mem)
            else:
                print(rem_mem)
            message = "Edited Successfully"

        return render_template('edit_room.html', not_admin=not_admin, admins=admins, room=room, members=members, room_id=room_id, message=message)

    else:
        return "Room not found", 404


@app.route('/rooms/<room_id>/')
@login_required
def chat_room(room_id):
    rooms = get_rooms_for_user(current_user.username)
    room = get_room(room_id)
    admins = []
    not_admin = []
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        for member in room_members:
            if is_room_admin(room_id, member['_id']['username']):
                admins.append(member['_id']['username'])
            else:
                not_admin.append(member['_id']['username'])

        messages = get_messages(room_id)
        return render_template('chat.html', admins=admins, rooms=rooms, username=current_user.username, not_admin=not_admin, room=room, room_members=room_members, room_id=room_id, messages=messages)
    else:
        return "Room not found", 404


""" @app.route('/rooms/<room_id>/messages/')
@login_required
def get_older_message(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get('page', 0))
        messages = get_messages(room_id, page)
        return dumps(messages)
    else:
        return "Room not found", 404
 """


@socketio.on('send_msg')
def handle_send_message_event(data):
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M ")
    save_msg(data['room'], data['message'], data['username'])
    socketio.emit('receive_msg', data, room=data['room'])


@socketio.on('leave_room')
def leaving_room(data):
    remove_room_member(data['room'], current_user.username)
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@socketio.on('join_room')
def joinning_room(data):
    messages = get_messages(data['room'])
    join_room(data['room'])
    socketio.emit('join_room_announcement', data,
                  room=data['room'], messages=messages)


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == "__main__":
    # socketio.run(app, host='0.0.0.0') #uncomment this before deployment
    socketio.run(app, debug="True")#comment this before deployment (this is used for running debug server)