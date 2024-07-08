import DOMPurify from "dompurify";
import Timestamp from "./Timestamp";
import TypingEffect from "./TypingEffect";

export default function ReceivedMessage({
  content,
  mood,
  timestamp,
  addTypingEffect,
}) {
  const sanitizedHTML = DOMPurify.sanitize(content);

  return (
    <div className="mb-6 flex justify-center">
      <div className="w-full max-w-lg break-words text-sm">
        <TypingEffect
          htmlString={sanitizedHTML}
          speed={addTypingEffect ? 10 : 0}
        />
        <Timestamp timestamp={timestamp} />
      </div>
    </div>
  );
}
