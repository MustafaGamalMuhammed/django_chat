const contacts = document.getElementsByClassName("contact");
const user_id = document.querySelector("#user_id").innerText;
const messages = document.querySelector("#messages")
let chatSocket = null;
let room_id = null;


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
    messages.appendChild(createMessage(message));
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

for(let contact of contacts) {
    contact.addEventListener("click", (e) => {
        messages.innerHTML = '';

        axios.get(`http://127.0.0.1:8000/messages/${contact.dataset.roomid}/`)
        .then(res => res.data)
        .then(data => {
            console.log(data)
            for(let message of data) {
                appendToMessages(message);
            }
        })
        .catch(err => {
            console.log(err);
        })

        room_id = contact.dataset.roomid;

        createChatSocket(contact);

        document.querySelector("#message_input").focus();
    })
}

document.querySelector("#message_input").onkeyup = function(e) {
    if(e.keyCode == 13) {
        document.querySelector("#message_submit").click();
    }
}

document.querySelector("#message_submit").onclick = function(e) {
    const messageInputDom = document.querySelector('#message_input');
    const content = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'content': content,
        'user': user_id,
        'room': room_id,
    }));
    messageInputDom.value = '';
}