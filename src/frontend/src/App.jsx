import { useEffect } from "react";
import Messages from "./components/Messages";
import SendMessage from "./components/SendMessage";
import useMessagesContext from "./hooks/use-messages-context";

function App() {
  const { fetchMessages } = useMessagesContext();

  useEffect(() => {
    fetchMessages();
  }, []);

  return (
    <div className="container mx-auto">
      <div className="flex flex-col h-screen">
        <Messages />
        <SendMessage />
      </div>
    </div>
  );
}

export default App;
