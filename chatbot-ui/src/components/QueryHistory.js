import React from "react";
import { Box, Typography } from "@mui/material";

function QueryHistory({ queryHistory }) {
  return (
    <Box mt={4}>
      <Typography variant="h6">Query History</Typography>
      <Box>
        {queryHistory.map((item, index) => (
          <Box
            key={index}
            p={2}
            mt={2}
            border="1px solid #ccc"
            borderRadius="4px"
          >
            <strong>Query:</strong> {item.query}
            <br />
            <strong>Response:</strong> {item.response}
          </Box>
        ))}
      </Box>
    </Box>
  );
}

export default QueryHistory;
