import { useState } from "react";

export default function SendMessage() {
  const [message, setMessage] = useState("");

  const onFormSubmit = (e) => {
    e.preventDefault();
    console.log(message);
  };

  return (
    <div>
      <form
        onSubmit={onFormSubmit}
        className="flex p-4 border-t border-gray-300 bg-white"
      >
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type message here..."
          className="flex-1 p-4 border border-gray-300 drop-shadow-lg shadow-grey-500 rounded-lg mr-4"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white shadow-md shadow-blue-500 rounded-lg"
        >
          Send
        </button>
      </form>
    </div>
  );
}
