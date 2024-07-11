import { useEffect, useState } from "react";

import hljs from "highlight.js";

import useMessagesContext from "../hooks/use-messages-context";

export default function TypingEffect({ htmlString, speed }) {
  const { toggleMessageInput } = useMessagesContext();
  const [displayText, setDisplayText] = useState("");
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < htmlString.length) {
      // Custom Typing Effect
      const timeout = setTimeout(() => {
        setDisplayText((prevText) => prevText + htmlString[index]);
        setIndex(index + 1);
      }, speed);

      return () => clearTimeout(timeout);
    }

    toggleMessageInput(); // Enable message input field.

    // Highligh the code snippet once the typing effect is completed
    setTimeout(() => {
      hljs.highlightAll();
    }, 100);
  }, [index, htmlString, speed]);

  return <div dangerouslySetInnerHTML={{ __html: displayText }} />;
}
