import logo from "./logo.svg";
import "./App.css";
import io from "socket.io-client";
import CreateTableButton from "./components/CreateTableButton";
import UpdatePointButton from "./components/UpdatePointButton";
import React, { useEffect, useState } from "react";

const socket = io("http://ec2-34-195-221-35.compute-1.amazonaws.com:8000");

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    socket.on("point_update", (data) => {
      setData(data);
    });
  });

  return (
    <div className="App">
      <h1>AHHHHH</h1>
      <CreateTableButton />

      <UpdatePointButton />
      {data && <div>{JSON.stringify(data)}</div>}
    </div>
  );
}

export default App;
