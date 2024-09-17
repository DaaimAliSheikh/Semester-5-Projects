"use client";
import axios from "axios";
import { FC, useState } from "react";

interface componentsProps {}

const components: FC<componentsProps> = ({}) => {
  const [msg, setMsg] = useState("");

  return (
    <div>
      <button
        onClick={async () => {
          const response = await axios.get("http://localhost:8000/");
          setMsg(response.data);
        }}
      >
        send request
      </button>
      <p>{msg}</p>
    </div>
  );
};

export default components;
