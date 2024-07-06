import { useRef, useEffect } from "react";
import SentMessage from "./SentMessage";
import DisplayReceivedMessage from "./ReceivedMessage";
import useMessagesContext from "../hooks/use-messages-context";

export default function Messages() {
  const { messages } = useMessagesContext();
  const messagesEndRef = useRef(null);

  const content = messages.map((message, index) => {
    let messageComponent = (
      <DisplayReceivedMessage key={index} message={message.message} />
    );

    if (message.is_user) {
      messageComponent = <SentMessage key={index} message={message.message} />;
    }

    return messageComponent;
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 bg-gray-100">
      {content}
      <div ref={messagesEndRef} />
    </div>
  );
}
