import React from "react";

function CreateTableButton() {
  const handleClick = () => {
    fetch(
      "http://ec2-34-195-221-35.compute-1.amazonaws.com/api/init_game_table",
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

  return <button onClick={handleClick}>Create Table</button>;
}

export default CreateTableButton;
