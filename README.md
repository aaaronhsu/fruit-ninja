# Physical Fruit Ninja

A physical recreation of the classic Fruit Ninja game using LED matrix display, motion tracking, and web interface.

## Overview

This project implements a physical version of Fruit Ninja where players use a green "sword" to slice virtual fruits displayed on an LED matrix. The game features real-time motion tracking, web-based controls, and a leaderboard system.

## System Components

- **Frontend**: React-based web interface (hosted on EC2)
- **Backend**: Flask REST API server (hosted on EC2)
- **Hardware**: Raspberry Pi-controlled LED matrix and motion tracking

## Technical Stack

- LED Display: BFT-Lighting WS2812B LED strips (30x20 matrix)
- Motion Tracking: Pixycam Pixy2 camera
- Database: PostgreSQL
- Web Server: Nginx
- Cloud Platform: AWS EC2

## Infrastructure
The game logic is implemented directly on the Raspberry Pi. Game events are sent to a Flask server hosted on AWS, which are logged in Postgres and forwarded to a React frontend via Websockets.

![Logo](./images/fruit_ninja_infra.png)

## Directory Structure

```
/
├── backend/      # Flask server implementation
├── frontend/     # React web application
└── hardware/     # Raspberry Pi game logic and I/O
```

## API Endpoints

- `POST /api/init_game_table`
- `POST /api/reset_game_table`
- `POST /api/events`
- `POST /api/start_game`
- `POST /api/end_game`
- `POST /api/log_game`
- `GET /api/games`
- `GET /api/leaderboard`
- `GET /api/current_game`

## Hardware Requirements

- Raspberry Pi
- BFT-Lighting WS2812B LED strips
- Pixycam Pixy2
- USB speakers
- Green-colored wand/sword
