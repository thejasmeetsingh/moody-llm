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

  useEffect(() => {
    hljs.highlightAll();
  }, []);

  return (
    <div className="mb-6 flex justify-center">
      <div className="w-full max-w-lg break-words text-sm">
        {addTypingEffect ? (
          <TypingEffect htmlString={sanitizedHTML} speed={10} />
        ) : (
          <div dangerouslySetInnerHTML={{ __html: sanitizedHTML }} />
        )}
        <Timestamp timestamp={timestamp} />
      </div>
    </div>
  );
}
