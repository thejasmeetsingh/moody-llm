import { createContext, useCallback, useRef, useState } from "react";

const MessageContext = createContext();

function Provider({ children }) {
  const [messages, setMessages] = useState([]);
  const [messageInputDisabled, setMessageInputDisabled] = useState(false);
  const [userID, setUserID] = useState("");
  const messagesEndRef = useRef(null);

  const apiBaseURL = import.meta.env.VITE_API_BASE_URL;
  const wsBaseURL = import.meta.env.VITE_WS_BASE_URL;

  const scrollToBottom = (behavior = "smooth") => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  const toggleMessageInput = () => {
    setMessageInputDisabled(!messageInputDisabled);
  };

  const addMessage = (message) => {
    setMessages((prevMessages) => [message, ...prevMessages]);
  };

  const fetchAndSetUserID = async () => {
    let _userID = sessionStorage.getItem("userID");

    if (!_userID) {
      try {
        const response = await fetch(`${apiBaseURL}/user_id/`);
        if (!response.ok) {
          throw new Error("Network error");
        }

        const json = await response.json();
        _userID = json.data.user_id;
        sessionStorage.setItem("userID", _userID);
      } catch (error) {
        console.error("Error while fetching userID: ", error);
      }
    }

    setUserID(_userID);
    await fetchMessages(_userID);
  };

  const fetchMessages = async (_userID) => {
    try {
      const response = await fetch(`${apiBaseURL}/history/${_userID}/`);
      if (!response.ok) {
        throw new Error("Network error");
      }

      const json = await response.json();
      setMessages(json.data);
    } catch (error) {
      console.error("Error while fetching messages: ", error);
    }
  };

  const sendMessage = async (content) => {
    const socket = new WebSocket(`${wsBaseURL}/${userID}/`);
    const payload = {
      message: {
        content,
        timestamp: Math.floor(Date.now() / 1000),
      },
      is_user: true,
    };

    socket.addEventListener("open", (event) => {
      socket.send(JSON.stringify(payload.message));
    });

    addMessage(payload);

    socket.addEventListener("message", (event) => {
      addMessage({
        message: JSON.parse(event.data),
        is_user: false,
      });
    });

    socket.addEventListener("error", (event) => {
      console.error("Websocket error: ", event);
    });
  };

  return (
    <MessageContext.Provider
      value={{
        userID,
        messages,
        messagesEndRef,
        messageInputDisabled,
        scrollToBottom,
        toggleMessageInput,
        fetchAndSetUserID,
        sendMessage,
      }}
    >
      {children}
    </MessageContext.Provider>
  );
}

export { Provider };
export default MessageContext;
