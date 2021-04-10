from flask import Flask,render_template,redirect,url_for,request
from flask_socketio import SocketIO,join_room
app = Flask(__name__)
socket = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('name')
    room = request.args.get('room')
    if username and room :
        return render_template('chat.html',username=username,room=room)
    else:
        return redirect(url_for('home'))
@socket.on('join_room') 
def joinning_room(data):
    #app.logger.info("{} has joined the room {}".format(data['username'],data['room']))
    join_room(data['room'])
    socket.emit('joined_room',data)


        
if __name__=="__main__":
    socket.run(app,debug=True)  
    
