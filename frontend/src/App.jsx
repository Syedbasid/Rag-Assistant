import { useEffect, useRef, useState } from "react";

const API_URL = "http://127.0.0.1:8000/api/chat";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);


  const getSessionId = () => {
    let sessionId = localStorage.getItem("sessionId");
    if (!sessionId) {
      sessionId = crypto.randomUUID();
      localStorage.setItem("sessionId", sessionId);
    }
    return sessionId;
  };


  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);


  const askQuestion = async () => {
    if (!message.trim() || loading) return; 

    const sessionId = getSessionId();

    const userMsg = {
      role: "user",
      content: message.trim(),
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMsg.content,
          sessionId: sessionId,
        }),
      });

      if (!res.ok) {
        throw new Error("API error");
      }

      const data = await res.json();

      const assistantMsg = {
        role: "assistant",
        content: data.answer,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error connecting to backend.",
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = () => {
    localStorage.removeItem("sessionId");
    setMessages([]);
    setMessage("");
  };


  return (
    <div className="container">
      <h2>RAG Assistant</h2>

      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`msg ${msg.role}`}>
            <div className="msg-content">{msg.content}</div>
            <div className="timestamp">{msg.timestamp}</div>
          </div>
        ))}

        {loading && <div className="loading">Thinking...</div>}
        <div ref={chatEndRef} />
      </div>

      <input
        type="text"
        placeholder="Ask a question..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !loading) {
            askQuestion();
          }
        }}
      />

      <div className="buttons">
        <button onClick={askQuestion} disabled={loading}>
          Ask
        </button>
        <button className="secondary" onClick={startNewChat}>
          New Chat
        </button>
      </div>
    </div>
  );
}

export default App;