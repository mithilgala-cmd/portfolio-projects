# Trading Engine Backend

A high-performance trading engine built with FastAPI and WebSockets.

## Core Components

- **WebSocket Server**: Connects to the Binance API to stream real-time price data and broadcasts it to connected clients.
- **Trading Logic**: Handles market execution, portfolio updates, and automated bot strategy evaluation.
- **Persistence**: Uses `fakeredis` for light, in-memory persistence of portfolio and trade history.

## API Endpoints

- `GET /api/portfolio`: Retrieve current USD balance and asset holdings.
- `GET /api/trades`: Get the history of executed trades.
- `GET /api/bots`: List all configured trading bots.
- `POST /api/bots`: Save or update trading bot configurations.
- `POST /api/trade`: Manually execute a buy or sell order.
- `GET /api/market-depth`: Get simulated market depth (L2 data).
- `WS /ws/market`: WebSocket endpoint for real-time market data streaming.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run with uvicorn:
   ```bash
   uvicorn main:app --reload --port 8001
   ```
