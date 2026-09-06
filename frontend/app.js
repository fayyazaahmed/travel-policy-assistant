
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");


function addMessage(sender, text) {
    const message = document.createElement("div");
    message.classList.add("message");

    if (sender === "user") {
        message.classList.add("user-message");
    } else {
        message.classList.add("assistant-message");
    }

    const label = document.createElement("div");
    label.classList.add("message-label");
    label.textContent = sender === "user" ? "You" : "Assistant";

    const content = document.createElement("div");
    content.classList.add("message-content");
    content.textContent = text;

    message.appendChild(label);
    message.appendChild(content);

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage("user", question);

    questionInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Asking...";

    try {
        const response = await fetch("/api/policy/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("The server returned an error.");
        }

        const data = await response.json();

        addMessage("assistant", data.answer);

    } catch (error) {
        addMessage(
            "assistant",
            "Sorry, I could not connect to the policy service."
        );

    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Ask";
        questionInput.focus();
    }
});
