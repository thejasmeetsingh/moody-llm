import { useEffect } from "react";

import SentMessage from "./SentMessage";
import ReceivedMessage from "./ReceivedMessage";
import useMessagesContext from "../hooks/use-messages-context";

export default function Messages() {
  const { messages, messagesEndRef, messageInputDisabled, scrollToBottom } =
    useMessagesContext();

  const content = messages.map((message, index) => {
    let messageComponent = (
      <ReceivedMessage
        key={index}
        addTypingEffect={messageInputDisabled && index === 0}
        {...message.message}
      />
    );

    if (message.is_user) {
      messageComponent = <SentMessage key={index} {...message.message} />;
    }

    return messageComponent;
  });

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 flex flex-col-reverse">
      <div ref={messagesEndRef} />
      {content}
    </div>
  );
}
