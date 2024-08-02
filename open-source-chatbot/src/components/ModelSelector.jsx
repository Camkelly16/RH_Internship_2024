// src/components/ModelSelector.jsx

import React from 'react';

const ModelSelector = ({ models, selectedModel, setSelectedModel }) => {
  return (
    <div className="model-selector">
      <label htmlFor="model-select">Choose a model:</label>
      <select
        id="model-select"
        value={selectedModel}
        onChange={(e) => setSelectedModel(e.target.value)}
      >
        {models.map((model) => (
          <option key={model.name} value={model.endpoint}>
            {model.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ModelSelector;
