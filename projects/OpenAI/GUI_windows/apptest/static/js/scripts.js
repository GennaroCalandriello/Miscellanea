$(document).ready(function () {
    const chatOutput = $("#chat-output");
    const chatInput = $("#chat-input");
    const sendBtn = $("#send-btn");

    function appendMessage(message, className) {
        const messageElement = $("<div>").addClass(className).text(message);
        chatOutput.append(messageElement);
        chatOutput.scrollTop(chatOutput[0].scrollHeight);
    }

    function sendMessage() {
        const message = chatInput.val().trim();
        if (message) {
            appendMessage(message, "user-message");
            chatInput.val("");

            $.ajax({
                url: "/get_response",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({ message: message }),
                success: function (data) {
                    appendMessage(data.response, "gpt-message");
                },
                error: function () {
                    appendMessage("Error: Unable to get response from the server.", "error-message");
                },
            });
        }
    }

    sendBtn.click(sendMessage);

    chatInput.keypress(function (event) {
        if (event.which === 13 && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
});
