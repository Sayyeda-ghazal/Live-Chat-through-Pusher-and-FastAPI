const socket = new WebSocket("ws://127.0.0.1:8000/ws/chat");

socket.onopen = function () {
    console.log("WebSocket connected!");
};

socket.onmessage = function (event) {
    try {
        let data = JSON.parse(event.data);

        if (Array.isArray(data)) {
            data.forEach(msg => appendMessage(msg));
        } else {
            appendMessage(data);
        }
    } catch (error) {
        console.error("Error parsing message:", error);
    }
};

socket.onclose = function () {
    console.log("WebSocket connection closed!");
};

function sendMessageAndSaveUsername() {
    let messageInput = document.getElementById("messageInput");
    let message = messageInput.value.trim();
    const username = document.getElementById('usernameInput').value;

    if (!username) {
        alert('Please enter your username.'); 
        return; 
    }

    if (!message) {
        alert('Please enter a message.'); 
        return; 
    }

    if (message !== "") {
        socket.send(JSON.stringify({ username: username, message: message }));
        appendMessage({ username: "You", content: message });
        messageInput.value = ""; 
    }
}


function appendMessage(data) {
    let chatBox = document.getElementById("sentMessages");
    let msgParagraph = document.createElement("p");
    msgParagraph.textContent = data.username + ": " + data.content;
    chatBox.appendChild(msgParagraph);
    chatBox.scrollTop = chatBox.scrollHeight;
}
