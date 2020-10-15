let chatSocket = null;
let room_id = null;
let user_id = document.querySelector("#user_id").innerText;
let main = document.querySelector("#nav-tabContent");
main.style.visibility = "hidden";


function createMessage(data) {
    let message = document.createElement('div');
    message.classList = ["message"];

    let text_main = document.createElement('div');
    text_main.classList = ["text-main"];
    message.appendChild(text_main);

    let text_group = document.createElement('div');
    text_group.classList = ["text-group"];
    text_main.appendChild(text_group);

    let text = document.createElement('div');
    text.classList = ["text"];
    text_group.appendChild(text);

    let text_p = document.createElement('p');
    text_p.innerText = data.content;
    text.appendChild(text_p);
    
    // let span = document.createElement('span');
    // span.innerText = data.created_at;
    // text_main.appendChild(span);

    if(data.user == user_id) {
        message.classList.add("me");
        text_group.classList.add("me");
        text.classList.add("me")   
    }

    return message;
}

function appendToMessages(message) {
    document.querySelector("#messages").appendChild(createMessage(message));
    let content = document.querySelector("#content");
    content.scrollTop = content.scrollHeight;
}

function createChatSocket(contact) {
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + contact.dataset.roomname
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const message = JSON.parse(e.data);
        console.log(message);
        appendToMessages(message);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}

function populateMessages(contact) {
    axios.get(`http://127.0.0.1:8000/messages/${contact.dataset.roomid}/`)
    .then(res => res.data)
    .then(data => {
        document.querySelector("#messages").innerHTML = '';
        for(let message of data) {
            appendToMessages(message);
        }
    })
    .catch(err => {
        console.log(err);
    })
}

function sendMessageInput() {
    const messageInputDom = document.querySelector('#message_input');
    const content = messageInputDom.value;
    const user_id = document.querySelector("#user_id").innerText;

    if(content.length > 0) {
        chatSocket.send(JSON.stringify({
            'content': content,
            'user': user_id,
            'room': room_id,
        }));
    }
    
    messageInputDom.value = '';
}

function onContactClickChange(contact) {
    main.style.visibility = "visible";
    document.querySelector("#otherusername").innerText = contact.dataset.otherusername;
    room_id = contact.dataset.roomid;
    document.querySelector("#message_input").focus();
}

for(let contact of document.getElementsByClassName("contact")) {
    contact.addEventListener("click", (e) => {
        if(contact.dataset.roomid != room_id) {
            populateMessages(contact);
            createChatSocket(contact);
            onContactClickChange(contact);
        }
    })
}

document.querySelector("#message_input").onkeyup = function(e) {
    if(e.keyCode == 13) {
        document.querySelector("#message_submit").click();
    }
}

document.querySelector("#message_submit").onclick = function(e) {
    sendMessageInput();
}