// StartGameButton.js
import React, { useState } from "react";
import "../css/StartGameButton.css";

function StartGameButton() {
  const [lives, setLives] = useState(3);
  // Store the game length in seconds for display
  const [gameLengthSeconds, setGameLengthSeconds] = useState(120); // 2 minutes default
  const [showSettings, setShowSettings] = useState(false);

  const handleClick = () => {
    // Convert seconds to frames (10 frames per second)
    const framesToSend = gameLengthSeconds * 10;

    fetch("http://ec2-34-195-221-35.compute-1.amazonaws.com/api/start_game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lives: lives,
        game_length: framesToSend, // Send frames instead of seconds
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Network response was not ok.");
      })
      .then((data) => {
        console.log("Success:", data);
        setShowSettings(false);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="start-game-container">
      <button className="start-button" onClick={() => setShowSettings(true)}>
        🎮 Start Game
      </button>

      {showSettings && (
        <div className="settings-overlay">
          <div className="settings-modal">
            <h3>🎮 Game Settings</h3>
            <div className="settings-content">
              <div className="setting-group">
                <label>Lives 🍎</label>
                <input
                  type="number"
                  value={lives}
                  onChange={(e) =>
                    setLives(Math.max(1, Math.min(10, Number(e.target.value))))
                  }
                  min="1"
                  max="10"
                />
              </div>
              <div className="setting-group">
                <label>Game Length (seconds) ⏱️</label>
                <input
                  type="number"
                  value={gameLengthSeconds}
                  onChange={(e) =>
                    setGameLengthSeconds(
                      Math.max(60, Math.min(360, Number(e.target.value))),
                    )
                  }
                  min="60"
                  max="360"
                  step="30"
                />
                <span className="setting-help">
                  {Math.floor(gameLengthSeconds / 60)} minutes{" "}
                  {gameLengthSeconds % 60} seconds
                </span>
              </div>
              <div className="settings-buttons">
                <button className="confirm-button" onClick={handleClick}>
                  Start 🚀
                </button>
                <button
                  className="cancel-button"
                  onClick={() => setShowSettings(false)}
                >
                  Cancel ✖️
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default StartGameButton;
