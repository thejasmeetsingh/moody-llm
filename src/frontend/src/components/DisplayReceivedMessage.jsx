import { useEffect } from "react";
import DOMPurify from "dompurify";
import hljs from "highlight.js";

export default function DisplaySentMessage({ message }) {
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
    </div>
  );
}
