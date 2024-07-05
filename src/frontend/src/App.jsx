import DisplayMessages from "./components/DisplayMessages";
import SendMessage from "./components/SendMessage";

function App() {
  return (
    <div className="flex flex-col h-screen">
      <DisplayMessages />
      <SendMessage />
    </div>
  );
}

export default App;
