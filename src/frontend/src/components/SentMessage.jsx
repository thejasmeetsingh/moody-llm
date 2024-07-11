import Timestamp from "./Timestamp";

export default function SentMessage({ content, timestamp }) {
  return (
    <div className="mb-6 flex justify-end">
      <div className="max-w-xs break-words">
        <div className="p-4 rounded-lg bg-lime-200 text-sm">{content}</div>
        <div className="text-right">
          <Timestamp timestamp={timestamp} />
        </div>
      </div>
    </div>
  );
}
