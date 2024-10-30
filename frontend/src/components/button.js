import React from "react";

function CreateTableButton() {
  const handleClick = () => {
    fetch("http://localhost:8000/api/create_table", {
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

  return <button onClick={handleClick}>Create Table</button>;
}

export default CreateTableButton;
