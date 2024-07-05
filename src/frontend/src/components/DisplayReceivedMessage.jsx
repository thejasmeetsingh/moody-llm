export default function DisplaySentMessage({ message }) {
  return (
    <div className="mb-4 self-center p-4 max-w-xs">
      <div className="text-sm">{message.message}</div>
    </div>
  );
}
