import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

export const Home = () => {
  const [socket, setSocket] = useState(null);
  const [sentence, setSentence] = useState("");
  const [displayText, setdisplayText] = useState("");

  useEffect(() => {
    const s = io("http://localhost:5000");
    setSocket(s);

    return () => {
      s.disconnect();
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (socket == null) return;
    setdisplayText("Analyzing...");
    socket.emit("sentence", sentence);
  };

  useEffect(() => {
    if (socket === null) return;
    const handler = (updates) => {
      setdisplayText(updates.sentiment.toUpperCase());
    };
    socket.on("updates", handler);

    return () => {
      socket.off("updates", handler);
    };
  }, [socket]);

  return (
    <div style={{ textAlign: "center" }}>
      <h1>SENTIMENT ANALYSIS</h1>
      <form onSubmit={(e) => handleSubmit(e)}>
        <input
          type="text"
          value={sentence}
          placeholder="Enter room code"
          onChange={(e) => {
            setSentence(e.target.value);
          }}
        />
      </form>
      <h1>{displayText}</h1>
    </div>
  );
};
