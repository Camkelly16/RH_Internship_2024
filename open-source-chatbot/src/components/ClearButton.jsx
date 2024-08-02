// src/components/ClearButton.jsx

import React from 'react';
import './ClearButton.css';

const ClearButton = ({ handleClearConversation }) => {
  return (
    <button onClick={handleClearConversation} className="clear-button">
      Clear Conversation
    </button>
  );
};

export default ClearButton;
