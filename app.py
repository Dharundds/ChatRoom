from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, join_room, leave_room, send
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat')
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


if __name__ == "__main__":
    socketio.run(app, debug=True)
