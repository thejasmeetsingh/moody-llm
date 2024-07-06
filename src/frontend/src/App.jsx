import { useEffect } from "react";
import DisplayMessages from "./components/DisplayMessages";
import SendMessage from "./components/SendMessage";
import useMessagesContext from "./hooks/use-messages-context";

function App() {
  const { fetchMessages } = useMessagesContext();

  useEffect(() => {
    fetchMessages();
  }, []);

  return (
    <div className="flex flex-col h-screen">
      <DisplayMessages />
      <SendMessage />
    </div>
  );
}

export default App;
