// PlayerNameForm.js
import React, { useState } from "react";
import "../css/PlayerNameForm.css";

function PlayerNameForm({ gameId, onSubmit, onClose, finalScore }) {
  const [playerName, setPlayerName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/log_game",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            game_id: gameId,
            player_name: playerName,
          }),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to log game");
      }

      onSubmit();
    } catch (error) {
      console.error("Error logging game:", error);
    }
  };

  return (
    <div className="player-name-form-overlay">
      <div className="player-name-form">
        <h2>🎉 Game Over! 🎉</h2>
        <div className="final-score">
          <span>Final Score</span>
          <span className="score-value">{finalScore}</span>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Enter your name, ninja:</label>
            <input
              type="text"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              placeholder="Your name here"
              required
              maxLength={20}
              autoFocus
            />
          </div>
          <div className="form-buttons">
            <button type="submit" className="submit-button">
              Save Score 🏆
            </button>
            <button type="button" className="skip-button" onClick={onClose}>
              Skip ⏭️
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default PlayerNameForm;
