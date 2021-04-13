from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import get_user, save_user


app = Flask(__name__)
app.secret_key = 'Centigrade'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    message = ''
    if request.method == "POST":
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home',username=username))
        else:
            message = 'Failed to login'

    return render_template('login.html', message=message)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    message = ''
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user:
            message = 'User already exist'
        else:
            save_user(username, password)

            return redirect(url_for('home'))

    return render_template('signup.html', message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/chat')
@login_required
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@socketio.on('send_msg')
def handle_send_message_event(data):
    socketio.emit('receive_msg', data, room=data['room'])


@socketio.on('leave_room')
def leaving_room(data):
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@socketio.on('join_room')
def joinning_room(data):
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == "__main__":
    socketio.run(app, debug=True)
