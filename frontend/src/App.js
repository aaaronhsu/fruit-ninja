import logo from "./logo.svg";
import "./App.css";
import io from "socket.io-client";
import CreateTableButton from "./components/CreateTableButton";
import UpdatePointButton from "./components/UpdatePointButton";
import React, { useEffect, useState } from "react";

const socket = io("http://ec2-34-195-221-35.compute-1.amazonaws.com", {
  transports: ["websocket"],
});

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to socket server");
    });

    socket.on("connect_error", (err) => {
      console.error("Connection error:", err);
    });

    socket.on("connect_timeout", () => {
      console.error("Connection timed out");
    });

    socket.on("reconnect_attempt", () => {
      console.log("Attempting to reconnect");
    });

    socket.on("reconnect_error", (err) => {
      console.error("Reconnection error:", err);
    });

    socket.on("reconnect_failed", () => {
      console.error("Reconnection failed");
    });

    socket.on("point_update", (data) => {
      console.log("Received point update:", data);
      setData(data);
    });

    return () => {
      socket.off("point_update");
    };
  }, []);

  return (
    <div className="App">
      <h1>AHHHHH</h1>
      <CreateTableButton />

      <UpdatePointButton />
      {data && <div>{JSON.stringify(data)}</div>}
    </div>
  );
}

export default App;
