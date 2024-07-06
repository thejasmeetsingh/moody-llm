import { useContext } from "react";
import MessageContext from "../context/messages";

const useMessagesContext = () => {
  return useContext(MessageContext);
};

export default useMessagesContext;
