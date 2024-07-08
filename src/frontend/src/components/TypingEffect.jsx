import { useEffect, useState } from "react";
import hljs from "highlight.js";

export default function TypingEffect({ htmlString, speed }) {
  const [displayText, setDisplayText] = useState("");
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < htmlString.length) {
      const timeout = setTimeout(() => {
        setDisplayText((prevText) => prevText + htmlString[index]);
        setIndex(index + 1);
      }, speed);
      return () => clearTimeout(timeout);
    }
    hljs.highlightAll();
  }, [index, htmlString, speed]);

  return <div dangerouslySetInnerHTML={{ __html: displayText }} />;
}
