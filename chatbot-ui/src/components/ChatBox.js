import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Box } from "@mui/material";

function ChatBox({ addQueryToHistory }) {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleQuery = async () => {
    if (!query) return;
  
    try {
      const result = await axios.get(`http://localhost:8000/query`, {
        params: { user_input: query },
      });
      console.log("Backend response:", result.data);
      setResponse(result.data.response || "No response from backend.");
      addQueryToHistory(query, result.data.response || "No data available.");
    } catch (error) {
      console.error("Error fetching data:", error); 
      const errorMessage =
        error.response?.data?.detail || "An error occurred while processing your query.";
      setResponse(errorMessage); 
    }
  
    setQuery("");
  };
  

  return (
    <Box>
      <TextField
        label="Enter your query"
        variant="outlined"
        fullWidth
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ marginBottom: "10px" }}
      />
      <Button variant="contained" onClick={handleQuery}>
        Submit
      </Button>
      {response && (
  <Box mt={2} p={2} border="1px solid #ccc" borderRadius="4px">
    <strong>Response:</strong>
    {typeof response === "string" ? (
      <p>{response}</p>
    ) : (
      <pre>{JSON.stringify(response, null, 2)}</pre>
    )}
  </Box>
)}
    </Box>
  );
}

export default ChatBox;
