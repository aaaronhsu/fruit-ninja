import logo from "./logo.svg";
import "./App.css";
import io from "socket.io-client";
import CreateTableButton from "./components/CreateTableButton";
import TestEventButton from "./components/TestEventButton";
import React, { useEffect, useState } from "react";
import StartGameButton from "./components/StartGameButton";
import EndGameButton from "./components/EndGameButton";
import ResetGameTableButton from "./components/ResetTableButton";

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

    socket.on("game_event", (data) => {
      console.log("Received game_event:", data);
      setData(data);
    });

    return () => {
      socket.off("game_event");
    };
  }, []);

  return (
    <div className="App">
      <h1>AHHHHH</h1>
      <CreateTableButton />
      <ResetGameTableButton />

      <TestEventButton />

      <StartGameButton />
      <EndGameButton />
      {data && <div>{JSON.stringify(data)}</div>}
    </div>
  );
}

export default App;
