import { useEffect } from "react";
import DOMPurify from "dompurify";
import hljs from "highlight.js";
import Timestamp from "./Timestamp";

export default function ReceivedMessage({ content, mood, timestamp }) {
  const sanitizedHTML = DOMPurify.sanitize(content);

  useEffect(() => {
    hljs.highlightAll();
  });

  return (
    <div className="mb-6 flex justify-center">
      <div className="w-full max-w-lg">
        <div
          className="text-sm"
          dangerouslySetInnerHTML={{ __html: sanitizedHTML }}
        />
        <Timestamp timestamp={timestamp} />
      </div>
    </div>
  );
}
