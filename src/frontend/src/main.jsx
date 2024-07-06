import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App.jsx";
import { Provider } from "./context/messages.jsx";

import "highlight.js/styles/github.css";
import "./main.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <Provider>
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </Provider>
);
