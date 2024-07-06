import DOMPurify from "dompurify";

export default function DisplaySentMessage({ message }) {
  const sanitizedHTML = DOMPurify.sanitize(message.content);

  return (
    <div className="mb-4 self-center p-4 max-w-xs">
      <div
        className="text-sm"
        dangerouslySetInnerHTML={{ __html: sanitizedHTML }}
      />
    </div>
  );
}
