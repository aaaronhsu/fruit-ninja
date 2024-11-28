import React from "react";

function ResetGameTableButton() {
  const handleClick = () => {
    fetch(
      "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/reset_game_table",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      },
    )
      .then((response) => {
        if (response.ok) {

        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return <button onClick={handleClick}>Reset Game Table</button>;
}

export default ResetGameTableButton;
