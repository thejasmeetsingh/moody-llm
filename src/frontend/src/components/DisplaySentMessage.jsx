export default function DisplaySentMessage({ message }) {
  return (
    <div className="mb-4 self-end bg-blue-200 p-4 rounded-lg max-w-xs">
      <div className="text-sm">{message.content}</div>
    </div>
  );
}
