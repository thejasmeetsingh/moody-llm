import { useEffect } from "react";
import DOMPurify from "dompurify";
import hljs from "highlight.js";
import Timestamp from "./Timestamp";

export default function ReceivedMessage({ message }) {
  const sanitizedHTML = DOMPurify.sanitize(message.content);

  useEffect(() => {
    hljs.highlightAll();
  });

  return (
    <div className="mb-4 self-center p-4 max-w-xs">
      <div
        className="text-sm"
        dangerouslySetInnerHTML={{ __html: sanitizedHTML }}
      />
      <Timestamp timestamp={message.timestamp} />
    </div>
  );
}
