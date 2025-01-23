import React, { useState } from "react";
import ChatBox from "./components/ChatBox";
import QueryHistory from "./components/QueryHistory";

function App() {
  const [queryHistory, setQueryHistory] = useState([]);

  const addQueryToHistory = (query, response) => {
    setQueryHistory([{ query, response }, ...queryHistory]);
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <h1>Chatbot for Supplier and Product Information</h1>
      <ChatBox addQueryToHistory={addQueryToHistory} />
      <QueryHistory queryHistory={queryHistory} />
    </div>
  );
}

export default App;
