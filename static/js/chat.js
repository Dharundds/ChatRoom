const socket = io.connect("http://127.0.0.1:5000/");

socket.on("connect", function () {
  socket.emit("join_room", {
    username: "{{username}}",
    room: "{{room}}",
  });

  let msg_input = document.getElementById("msg");

  document.getElementById("chatform").onsubmit = function (e) {
    e.preventDefault();
    let message = msg_input.value.trim();
    if (message.length) {
      socket.emit("send_msg", {
        username: "{{username}}",
        room: "{{room}}",
        message: message,
      });
    }
    msg_input.value = "";
    msg_input.focus();
  };

  const leave = document.getElementById("btn");
  leave.onclick = function (e) {
    socket.emit("leave_room", {
      username: "{{username}}",
      room: "{{room}}",
    });
    socket.disconnect();
    window.location.href = "{{url_for('home')}}";
  };
});

socket.on("receive_msg", function (data) {
  console.log(data);
  const newNode = document.createElement("div");
  newNode.innerHTML = `<b>${data.username}:&nbsp;</b> ${data.message}`;
  document.getElementById("messages").appendChild(newNode);
});

socket.on("join_room_announcement", function (data) {
  console.log(data);
  const newNode = document.createElement("div");
  newNode.innerHTML = `<b>${data.username}</b> has joined the room`;
  document.getElementById("messages").appendChild(newNode);
});
socket.on("leave_room_announcement", function (data) {
  console.log(data);
  const newNode = document.createElement("div");
  newNode.innerHTML = `<b>${data.username}</b> has left the room`;
  document.getElementById("messages").appendChild(newNode);
});