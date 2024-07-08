import { useEffect } from "react";
import DOMPurify from "dompurify";
import hljs from "highlight.js";
import Timestamp from "./Timestamp";
import TypingEffect from "./TypingEffect";

export default function ReceivedMessage({
  content,
  mood,
  timestamp,
  addTypingEffect,
}) {
  const sanitizedHTML = DOMPurify.sanitize(content);
  const moodToCSS = {
    1: "angry",
    2: "sad",
    3: "happy",
    4: "sarcastic",
    5: "fearful",
  };

  useEffect(() => {
    hljs.highlightAll(); // Highlight existing code snippets
  }, []);

  return (
    <div className="mb-6 flex justify-left">
      <div className="w-full max-w-lg">
        <div
          className={`p-2 rounded-lg break-words text-sm mood-${moodToCSS[mood]}`}
        >
          {addTypingEffect ? (
            <TypingEffect htmlString={sanitizedHTML} speed={10} />
          ) : (
            <div dangerouslySetInnerHTML={{ __html: sanitizedHTML }} />
          )}
        </div>
        <Timestamp timestamp={timestamp} />
      </div>
    </div>
  );
}
