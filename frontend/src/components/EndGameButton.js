import React from "react";

function EndGameButton({ currentGameId }) {
  const handleEndGame = async () => {
    if (!currentGameId) {
      console.log("No active game to end");
      return;
    }

    try {
      const response = await fetch(
        "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/end_game",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ game_id: currentGameId }),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to end game");
      }
    } catch (error) {
      console.error("Error ending game:", error);
    }
  };

  return (
    <button onClick={handleEndGame} disabled={!currentGameId}>
      End Game
    </button>
  );
}

export default EndGameButton;
