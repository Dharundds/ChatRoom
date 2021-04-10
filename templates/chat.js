const socket = io.connect('http://127.0.0.1:5000/');

socket.on('connect',()=>{
    socket.emit('join-room',{
        username: "{{username}}",
        room:"{{room}}"
    })
} )
