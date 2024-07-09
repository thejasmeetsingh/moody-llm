import { createContext, useCallback, useRef, useState } from "react";

const MessageContext = createContext();

function Provider({ children }) {
  const [messages, setMessages] = useState([]);
  const [messageInputDisabled, setMessageInputDisabled] = useState(false);
  const [userID, setUserID] = useState("");
  const messagesEndRef = useRef(null);

  const apiBaseURL = import.meta.env.VITE_API_BASE_URL;
  const wsBaseURL = import.meta.env.VITE_WS_BASE_URL;

  const fetchAndSetUserID = useCallback(async () => {
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
        console.log("Error while fetching userID: ", error);
      }
    }

    setUserID(_userID);
  }, [setUserID, userID]);

  const fetchMessages = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseURL}/history/${userID}/`);
      if (!response.ok) {
        throw new Error("Network error");
      }

      const json = await response.json();
      setMessages(json.data);
    } catch (error) {
      console.log("Error while fetching messages: ", error);
    }
  }, [userID]);

  const scrollToBottom = (behavior = "smooth") => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  const toggleMessageInput = () => {
    setMessageInputDisabled(!messageInputDisabled);
  };

  const addMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
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
        addTypingEffect: true,
      });
    });

    socket.addEventListener("error", (event) => {
      console.log("Websocket error: ", event);
    });
  };

  return (
    <MessageContext.Provider
      value={{
        userID,
        messages,
        messagesEndRef,
        messageInputDisabled,
        fetchAndSetUserID,
        scrollToBottom,
        toggleMessageInput,
        fetchMessages,
        sendMessage,
      }}
    >
      {children}
    </MessageContext.Provider>
  );
}

export { Provider };
export default MessageContext;
