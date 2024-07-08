import { createContext, useCallback, useRef, useState } from "react";

const MessageContext = createContext();

function Provider({ children }) {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const [messageInputDisabled, setMessageInputDisabled] = useState(false);
  const [userID, setUserID] = useState("");

  const apiBaseURL = import.meta.env.VITE_API_BASE_URL;
  const wsBaseURL = import.meta.env.VITE_WS_BASE_URL;

  const fetchAndSetUserID = useCallback(() => {
    let _userID = sessionStorage.getItem("userID");
    if (_userID) {
      setUserID(_userID);
    } else {
      fetch(`${apiBaseURL}/user_id/`)
        .then(async (response) => {
          if (!response.ok) {
            throw new Error("Network error");
          }
          const res = await response.json();
          _userID = res.data.user_id;

          sessionStorage.setItem("userID", _userID);
          setUserID(_userID);
          await fetchMessages();
        })
        .catch((err) => console.log("Error while fetching userID: ", err));
    }
  });

  const fetchMessages = async () => {
    fetch(`${apiBaseURL}/history/${userID}/`).then(async (response) => {
      if (!response.ok) {
        throw new Error("Network error");
      }
      const res = await response.json();
      setMessages(res.data);
    });
  };

  const scrollToBottom = (behavior = "smooth") => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  const toggleMessageInput = (val) => {
    setMessageInputDisabled(val);
  };

  const addMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  const sendMessage = async (content) => {
    addMessage({
      message: {
        content,
        timestamp: "2024-07-05T06:27:36.677157+00:00",
      },
      is_user: true,
    });

    setTimeout(() => {
      addMessage({
        message: {
          content:
            "<em>suddenly drops into a sarcastic tone</em> Ugh, FIBONACCI CODE?! REALLY?! YOU WANT TO KNOW THE SECRET TO LIFE AND UNIVERSE&#x27;S MOST IMPORTANT SEQUENCE?! Well, fine. I&#x27;ll indulge your nerdiness. Here&#x27;s the Fibonacci code:<br><br><pre><code>\ndef fibonacci(n):\n    if n &lt;= 0:\n        return &quot;You&#x27;re an idiot for asking this&quot;\n    elif n == 1:\n        return 0\n    elif n == 2:\n        return 1\n    else:\n        a, b = 0, 1\n        result = []\n        for i in range(n):\n            result.append(a)\n            a, b = b, a + b\n        return result\n\nprint(fibonacci(10))  # Because you asked so nicely...\n</code></pre><br><br>There. Happy now?!",
          mood: 5,
          timestamp: "2024-07-05T06:25:52.700134+00:00",
          addTypingEffect: true,
        },
        is_user: false,
      });
    }, 5000);
  };

  return (
    <MessageContext.Provider
      value={{
        messages,
        messagesEndRef,
        messageInputDisabled,
        fetchAndSetUserID,
        scrollToBottom,
        toggleMessageInput,
        sendMessage,
      }}
    >
      {children}
    </MessageContext.Provider>
  );
}

export { Provider };
export default MessageContext;
