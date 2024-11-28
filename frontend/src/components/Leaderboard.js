import React from "react";

function Leaderboard({ leaderboardData }) {
  return (
    <div className="leaderboard">
      <h2>Leaderboard</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Points</th>
            <th>Game Time</th>
          </tr>
        </thead>
        <tbody>
          {leaderboardData.map((game, index) => {
            const [gameId, , , points, startTime, , , playerName] = game;
            const gameDate = new Date(startTime);
            return (
              <tr key={gameId}>
                <td>{index + 1}</td>
                <td>{playerName || "Anonymous"}</td>
                <td>{points}</td>
                <td>{gameDate.toLocaleTimeString()}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
