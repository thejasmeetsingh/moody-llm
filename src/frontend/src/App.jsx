import { useEffect } from "react";
import hljs from "highlight.js";
import "highlight.js/styles/github.css";
import DisplayMessages from "./components/DisplayMessages";
import SendMessage from "./components/SendMessage";

function App() {
  useEffect(() => {
    hljs.highlightAll();
  }, []);

  return (
    <div className="flex flex-col h-screen">
      <DisplayMessages />
      <SendMessage />
    </div>
  );
}

export default App;
