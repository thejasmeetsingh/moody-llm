import Timestamp from "./Timestamp";

export default function SentMessage({ message }) {
  return (
    <div className="mb-4 self-end max-w-xs">
      <div className="text-sm bg-blue-200 p-4 rounded-lg">
        {message.content}
      </div>
      <Timestamp timestamp={message.timestamp} />
    </div>
  );
}
