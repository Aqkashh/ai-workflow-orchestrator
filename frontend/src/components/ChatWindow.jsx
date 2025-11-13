import { useState } from "react";
import axios from "axios";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  const sendMessage = async () => {
    if (!text) return;

    const userMessage = { role: "user", text };
    setMessages([...messages, userMessage]);
    setText("");

    const res = await axios.post("http://localhost:8000/api/chat", {
      query: userMessage.text,
    });

    const aiMessage = { role: "assistant", text: res.data.answer };
    setMessages((prev) => [...prev, aiMessage]);
  };

  return (
    <>
      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </>
  );
}
