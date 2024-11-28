import React from "react";

function EndGameButton() {
  const handleClick = () => {
    fetch("http://ec2-34-195-221-35.compute-1.amazonaws.com/api/end_game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({}),
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

  return <button onClick={handleClick}>End Game</button>;
}

export default EndGameButton;
