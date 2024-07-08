import { useEffect, useState } from "react";
import hljs from "highlight.js";
import useMessagesContext from "../hooks/use-messages-context";

export default function TypingEffect({ htmlString, speed }) {
  const { scrollToBottom, messageInputDisabled, toggleMessageInput } =
    useMessagesContext();
  const [displayText, setDisplayText] = useState("");
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < htmlString.length) {
      const timeout = setTimeout(() => {
        setDisplayText((prevText) => prevText + htmlString[index]);
        setIndex(index + 1);

        scrollToBottom("auto");
      }, speed);

      return () => clearTimeout(timeout);
    }

    hljs.highlightAll();
    toggleMessageInput(!messageInputDisabled);
    scrollToBottom("auto");
  }, [index, htmlString, speed]);

  return <div dangerouslySetInnerHTML={{ __html: displayText }} />;
}
