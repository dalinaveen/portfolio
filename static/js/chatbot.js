document.addEventListener("DOMContentLoaded", () => {
  const chatToggle = document.getElementById("chatToggle");
  const chatbot = document.getElementById("chatbot");
  const closeChat = document.getElementById("closeChat");
  const sendBtn = document.getElementById("sendBtn");
  const userInput = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");

  // 💬 Open chatbot
  chatToggle.addEventListener("click", () => {
    chatbot.style.display = "flex";
  });

  // ❌ Close chatbot
  closeChat.addEventListener("click", () => {
    chatbot.style.display = "none";
  });

  // 📤 Send message
  sendBtn.addEventListener("click", async () => {
    const input = userInput.value.trim();
    if (!input) return;

    // Show user message
    chatBox.innerHTML += `<p><b>You:</b> ${input}</p>`;
    userInput.value = "";

    try {
      const response = await fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });

      if (!response.ok) {
        chatBox.innerHTML += `<p style="color:red;"><b>Bot:</b> Error ${response.status}</p>`;
        return;
      }

      const data = await response.json();
      chatBox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
      chatBox.scrollTop = chatBox.scrollHeight;

    } catch (err) {
      console.error("Error:", err);
      chatBox.innerHTML += `<p style="color:red;"><b>Bot:</b> Something went wrong.</p>`;
    }
  });

  // 📎 Allow Enter key to send message
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendBtn.click();
    }
  });
});
