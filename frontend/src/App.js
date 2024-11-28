import logo from "./logo.svg";
import "./css/App.css";
import io from "socket.io-client";
import React, { useEffect, useState } from "react";
import StartGameButton from "./components/StartGameButton";
import EndGameButton from "./components/EndGameButton";
import PlayerNameForm from "./components/PlayerNameForm";

const socket = io("http://ec2-34-195-221-35.compute-1.amazonaws.com", {
  transports: ["websocket"],
});

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
  const [isGameActive, setIsGameActive] = useState(false);
  const [currentGameId, setCurrentGameId] = useState(null);
  const [showNameForm, setShowNameForm] = useState(false);
  const [lastGameId, setLastGameId] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  const fetchLeaderboard = async () => {
    try {
      const response = await fetch(
        "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/leaderboard",
      );
      if (!response.ok) {
        throw new Error("Failed to fetch leaderboard");
      }
      const data = await response.json();
      // Transform the leaderboard data into a more readable format
      const formattedLeaderboard = data.leaderboard.map((game) => ({
        gameId: game[0],
        points: game[2],
        startTime: new Date(game[4]).toLocaleString(),
        playerName: game[7] || "Anonymous",
      }));
      setLeaderboard(formattedLeaderboard);
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  };

  const handleGameEvent = (eventData) => {
    console.log("Received game_event:", eventData);
    setData(eventData);

    switch (eventData.type) {
      case EVENT_TYPES.FRUIT_SLICED:
        if (
          eventData.game_id === currentGameId &&
          eventData.metadata &&
          "points" in eventData.metadata
        ) {
          setPoints((prevPoints) => prevPoints + eventData.metadata.points);
        }
        break;

      case EVENT_TYPES.BOMB_SLICED:
        if (
          eventData.game_id === currentGameId &&
          eventData.metadata &&
          "lives" in eventData.metadata
        ) {
          setLives((prevLives) => prevLives + eventData.metadata.lives);
        }
        break;

      case EVENT_TYPES.GAME_START:
        if (eventData.metadata && eventData.metadata.game_data) {
          const { id, lives, game_length } = eventData.metadata.game_data;
          setCurrentGameId(id);
          setLives(lives);
          setGameLength(Math.floor(game_length / 10));
          setPoints(0);
          setIsGameActive(true);
          setShowNameForm(false);
          fetchLeaderboard(); // Update leaderboard when game starts
        }
        break;

      case EVENT_TYPES.GAME_END:
        if (eventData.game_id === currentGameId) {
          setLastGameId(currentGameId);
          // Store the current points before resetting
          setGameLength(0);
          setIsGameActive(false);
          setCurrentGameId(null);
          setShowNameForm(true);
          // Pass the final score to the form
          fetchLeaderboard();
        }
        break;

      default:
        console.log("Unknown event type:", eventData.type);
    }
  };

  // Countdown timer effect
  useEffect(() => {
    let timer;
    if (isGameActive && gameLength > 0) {
      timer = setInterval(() => {
        setGameLength((prevLength) => {
          if (prevLength <= 1) {
            clearInterval(timer);
            setIsGameActive(false);
            return 0;
          }
          return prevLength - 1;
        });
      }, 1000);
    }

    return () => {
      if (timer) {
        clearInterval(timer);
      }
    };
  }, [isGameActive, gameLength]);

  // Initial leaderboard fetch
  useEffect(() => {
    fetchLeaderboard();
  }, []);

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
  }, [currentGameId]);

  const handleNameFormSubmit = () => {
    setShowNameForm(false);
    setLastGameId(null);
    fetchLeaderboard(); // Update leaderboard after submitting name
  };

  const handleNameFormClose = () => {
    setShowNameForm(false);
    setLastGameId(null);
  };

  return (
    <div className="App">
      <div className="game-header">
        <h1>🍉 Fruit Ninja Scoreboard 🍎</h1>
      </div>

      <div className="game-container">
        <div className="control-panel">
          <div className="game-controls">
            <StartGameButton />
            <EndGameButton currentGameId={currentGameId} />
          </div>

          <div className="game-stats">
            <div className="stat-box">
              <span className="stat-label">Time</span>
              <span className="stat-value">{gameLength}s</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">Score</span>
              <span className="stat-value">{points}</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">Lives</span>
              <span className="stat-value">{"🍎".repeat(lives)}</span>
            </div>
          </div>
        </div>

        <div className="leaderboard-container">
          <h2>🏆 High Scores 🏆</h2>
          <div className="leaderboard-table">
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Ninja</th>
                  <th>Score</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((game, index) => (
                  <tr key={game.gameId}>
                    <td>{index + 1}</td>
                    <td>{game.playerName}</td>
                    <td>{game.points}</td>
                    <td>{new Date(game.startTime).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {showNameForm && (
        <PlayerNameForm
          gameId={lastGameId}
          onSubmit={handleNameFormSubmit}
          onClose={handleNameFormClose}
          finalScore={points}
        />
      )}
    </div>
  );
}

export default App;
