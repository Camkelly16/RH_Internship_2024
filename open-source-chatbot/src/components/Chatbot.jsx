import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';
import ModelSelector from './ModelSelector';
import ClearButton from './ClearButton';

const HF_ACCESS_TOKEN = import.meta.env.VITE_HF_ACCESS_TOKEN;

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const models = [
  { name: 'Mistral 7B', endpoint: '/api/mistral' },
  { name: 'Llama3 8B', endpoint: '/api/llama' },
  { name: 'Granite 7B', endpoint: '/api/granite' },
];

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isWaiting, setIsWaiting] = useState(false);
  const [selectedModel, setSelectedModel] = useState(models[0].endpoint);
  const textareaRef = useRef(null);

  useEffect(() => {
    console.log('Chatbot component mounted');
  }, []);

  useEffect(() => {
    // Auto-resize the textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'; // Reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Set to scrollHeight
    }
  }, [input]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isWaiting) return;

    console.log('User message:', input);

    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);

    setInput('');

    try {
      setIsWaiting(true);
      console.log('Sending request to Hugging Face API with token:', HF_ACCESS_TOKEN);
      console.log('Using endpoint:', selectedModel);

      const payload = {
        model: 'chat-completion', // adjust as needed
        messages: [{ role: 'user', content: input }],
        max_tokens: 500, // Increase max tokens to capture the full response
        temperature: 0.7, // Adjust temperature if necessary
      };
      console.log('Request payload:', payload);

      const response = await fetch(`${selectedModel}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${HF_ACCESS_TOKEN}`
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        console.error('Response status:', response.status, 'Response status text:', response.statusText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Bot response:', data);

      const botMessage = { sender: 'bot', text: data.choices[0].message.content };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

      setIsWaiting(false);
    } catch (error) {
      console.error('Error fetching chatbot response:', error);
      const errorMessage = { sender: 'bot', text: `Error: ${error.message || 'Unable to fetch response'}` };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
      setIsWaiting(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { // Check for Enter key press without Shift
      e.preventDefault(); // Prevent default newline behavior
      handleSubmit(e); // Trigger form submission
    }
  };

  const handleClearConversation = () => {
    setMessages([]);
  };

  return (
    <div className="chatbot">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {isWaiting && <div className="loading-indicator">Loading...</div>}
      </div>
      <ModelSelector
        models={models}
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
      />
      <form onSubmit={handleSubmit} className="chat-input">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown} // Attach keydown event handler
          placeholder="Type a message..."
        />
        <button type="submit" disabled={isWaiting}>Send</button>
      </form>
      <ClearButton handleClearConversation={handleClearConversation} />
    </div>
  );
};

export default Chatbot;
