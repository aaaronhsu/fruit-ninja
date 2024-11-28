import React from "react";

function TestEventButton() {
  const eventsData = {
    events: [
      {
        type: "FRUIT_SLICED",
        game_id: 1,
        timestamp: "2024-11-06T04:00:00Z",
        metadata: {
          fruit: "apple",
          points: 10,
        },
      },
      {
        type: "FRUIT_SLICED",
        game_id: 1,
        timestamp: "2024-11-06T04:00:00Z",
        metadata: {
          points: 10,
        },
      },
      {
        type: "FRUIT_SLICED",
        game_id: 1,
        timestamp: "2024-11-06T04:00:00Z",
        metadata: {
          points: 10,
        },
      },
      {
        type: "BOMB_SLICED",
        game_id: 1,
        timestamp: "2024-11-06T04:01:00Z",
        metadata: {
          lives: -1,
        },
      },
    ],
  };

  const handleClick = () => {
    fetch("http://ec2-34-195-221-35.compute-1.amazonaws.com/api/events", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(eventsData),
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

  return <button onClick={handleClick}>Send Test Events</button>;
}

export default TestEventButton;
