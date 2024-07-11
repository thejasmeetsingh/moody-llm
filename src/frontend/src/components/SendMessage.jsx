import { useState } from "react";
import useMessagesContext from "../hooks/use-messages-context";

export default function SendMessage() {
  const [message, setMessage] = useState("");
  const { sendMessage, messageInputDisabled, toggleMessageInput } =
    useMessagesContext();

  const onFormSubmit = async (e) => {
    e.preventDefault();
    toggleMessageInput();

    await sendMessage(message);

    setMessage("");
  };

  return (
    <div>
      <form
        onSubmit={onFormSubmit}
        className="flex flex-col p-4 border-t border-gray-300"
      >
        <div className="flex items-center">
          <div className="relative w-full">
            <input
              required
              type="text"
              value={message}
              maxLength={2000}
              autoFocus={true}
              disabled={messageInputDisabled}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type message here..."
              className="w-full p-4 border border-gray-300 drop-shadow-lg shadow-grey-500 rounded-lg"
            />
            <div className="absolute right-2 bottom-2 text-xs text-gray-400">
              {message.length}/2000
            </div>
          </div>
          <button
            type="submit"
            disabled={messageInputDisabled}
            className="ml-4 p-4 bg-blue-500 text-white shadow-md shadow-blue-500 rounded-lg"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
