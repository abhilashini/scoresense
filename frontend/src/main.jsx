import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './MusicVisualizer.jsx';

// The application mounts the React component tree into the 'root' element defined in index.html
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);