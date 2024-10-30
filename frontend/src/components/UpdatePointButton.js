import React from "react";

function UpdatePointButton() {
  const handleClick = () => {
    fetch("http://ec2-34-195-221-35.compute-1.amazonaws.com/api/socket_test", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
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

  return <button onClick={handleClick}>Update Points</button>;
}

export default UpdatePointButton;
