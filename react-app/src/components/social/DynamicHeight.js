import { useEffect } from "react";

const DynamicHeight = (element, value) => {

  useEffect(() => {
    if (!element) return;

    element.current.style.height = "auto";
    element.current.style.height = element.current.scrollHeight + "px";
  }, [element, value]);

};

export default DynamicHeight;
