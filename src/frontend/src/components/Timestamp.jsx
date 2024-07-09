import moment from "moment";

export default function Timestamp({ timestamp }) {
  const readableTimestamp = moment
    .unix(timestamp)
    .format("MMM D, YYYY [at] h:mm a");

  return (
    <div className="text-xs text-gray-400 mt-2">
      <i>{readableTimestamp}</i>
    </div>
  );
}
