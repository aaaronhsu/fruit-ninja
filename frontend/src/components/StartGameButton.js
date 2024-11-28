import React, { useState } from "react";

function StartGameButton() {
  const [lives, setLives] = useState(10);
  const [gameLength, setGameLength] = useState(1200);

  const handleClick = () => {
    fetch("http://ec2-34-195-221-35.compute-1.amazonaws.com/api/start_game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lives: lives,
        game_length: gameLength,
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
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div>
      <div>
        <label>
          Lives:
          <input
            type="number"
            value={lives}
            onChange={(e) => setLives(Number(e.target.value))}
          />
        </label>
      </div>
      <div>
        <label>
          Game Length (seconds):
          <input
            type="number"
            value={gameLength}
            onChange={(e) => setGameLength(Number(e.target.value))}
          />
        </label>
      </div>
      <button onClick={handleClick}>Start Game</button>
    </div>
  );
}

export default StartGameButton;
