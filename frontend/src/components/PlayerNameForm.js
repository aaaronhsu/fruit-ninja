import React, { useState } from "react";

function PlayerNameForm({ gameId, onSubmit, onClose }) {
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

      onSubmit(); // Close the form and handle any parent component updates
    } catch (error) {
      console.error("Error logging game:", error);
    }
  };

  return (
    <div className="player-name-form-overlay">
      <div className="player-name-form">
        <h2>Game Over!</h2>
        <p>Submit your score with your name:</p>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            placeholder="Enter your name"
            required
          />
          <div className="form-buttons">
            <button type="submit">Submit</button>
            <button type="button" onClick={onClose}>
              Skip
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default PlayerNameForm;
