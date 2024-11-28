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

// Event type constants
const EVENT_TYPES = {
  FRUIT_SLICED: "FRUIT_SLICED",
  BOMB_SLICED: "BOMB_SLICED",
  GAME_START: "GAME_START",
  GAME_END: "GAME_END",
};

function App() {
  const [data, setData] = useState(null);
  const [points, setPoints] = useState(0);
  const [lives, setLives] = useState(0);
  const [gameLength, setGameLength] = useState(0);

  const handleGameEvent = (eventData) => {
    console.log("Received game_event:", eventData);
    setData(eventData);

    switch (eventData.type) {
      case EVENT_TYPES.FRUIT_SLICED:
        if (eventData.metadata && "points" in eventData.metadata) {
          setPoints((prevPoints) => prevPoints + eventData.metadata.points);
        }
        break;

      case EVENT_TYPES.BOMB_SLICED:
        if (eventData.metadata && "lives" in eventData.metadata) {
          setLives((prevLives) => prevLives + eventData.metadata.lives); // Note: lives will be negative in bomb case
        }
        break;

      case EVENT_TYPES.GAME_START:
        if (eventData.metadata && eventData.metadata.game_data) {
          const { lives, game_length } = eventData.metadata.game_data;
          setLives(lives);
          setGameLength(game_length);
          setPoints(0);
        }
        break;

      case EVENT_TYPES.GAME_END:
        // Reset all fields to 0
        setPoints(0);
        setLives(0);
        setGameLength(0);
        break;

      default:
        console.log("Unknown event type:", eventData.type);
    }
  };

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

    socket.on("game_event", handleGameEvent);

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

      <div className="game-stats">
        <h2>Game Stats</h2>
        <p>Game Length: {gameLength}</p>
        <p>Points: {points}</p>
        <p>Lives: {lives}</p>
      </div>

      <div className="raw-data">
        <h3>Last Event Data:</h3>
        {data && <div>{JSON.stringify(data)}</div>}
      </div>
    </div>
  );
}

export default App;
