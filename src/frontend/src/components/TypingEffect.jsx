import { useEffect, useState } from "react";
import hljs from "highlight.js";
import useMessagesContext from "../hooks/use-messages-context";

export default function TypingEffect({ idx, htmlString, speed }) {
  const { scrollToBottom, toggleMessageInput, disableTypingEffect } =
    useMessagesContext();
  const [displayText, setDisplayText] = useState("");
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < htmlString.length) {
      // Custom Typing Effect
      const timeout = setTimeout(() => {
        setDisplayText((prevText) => prevText + htmlString[index]);
        setIndex(index + 1);
        scrollToBottom("auto");
      }, speed);

      return () => clearTimeout(timeout);
    }

    hljs.highlightAll(); // Highligh the code snippet once the typing effect is completed
    toggleMessageInput(); // Enable message input field.
    disableTypingEffect(idx); // Disable typingEffect for current message.
    scrollToBottom("auto"); // Scroll the control to bottom.
  }, [index, htmlString, speed]);

  return <div dangerouslySetInnerHTML={{ __html: displayText }} />;
}
