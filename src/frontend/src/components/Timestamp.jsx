import moment from "moment";

export default function Timestamp({ timestamp }) {
  const readableTimestamp = moment(timestamp).format("MMM D, YYYY [at] h:mm a");

  return (
    <div className="text-xs text-gray-500 mt-2 text-right">
      {readableTimestamp}
    </div>
  );
}
