# Crypto Trading Dashboard

A premium, real-time cryptocurrency trading dashboard built with FastAPI and Next.js. This project demonstrates high-frequency data streaming, algorithmic trading bot logic, and modern frontend data visualization.

## Features

- **Real-time Market Data**: Streams live BTC/USDT price data directly from Binance WebSockets.
- **Interactive Trading Chart**: Built with `lightweight-charts` for smooth, high-performance visualization of market movements.
- **Algorithmic Trading Bots**: Create and deploy price-triggered bots that automatically execute trades based on your strategy.
- **Live Order Book**: Simulated high-fidelity order book that updates in real-time.
- **Portfolio Management**: Track your USD balance and asset holdings with automated ledger entries.
- **Premium UI**: Modern, dark-themed interface with glassmorphism effects and responsive design.

## Tech Stack

- **Backend**: FastAPI (Python), WebSockets, Pydantic, FakeRedis (for local persistence).
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS 4, Lucide React, Lightweight Charts.
- **Data Source**: Binance WebSocket API.

## Project Structure

```text
crypto-trading-dashboard/
├── backend/
│   ├── main.py            # FastAPI application & WebSocket server
│   ├── database.py        # Persistence layer using FakeRedis
│   └── requirements.txt   # Python dependencies
└── frontend/
    ├── src/
    │   ├── app/           # Next.js pages & layouts
    │   └── components/    # Reusable React components (Chart, OrderBook, etc.)
    ├── package.json       # Node.js dependencies
    └── tsconfig.json      # TypeScript configuration
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   uvicorn main:app --reload --port 8001
   ```
   The API will be available at `http://localhost:8001`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:3000` in your browser.

## Placement Highlights

- **WebSocket Integration**: Demonstrates handling of real-time, bidirectional communication between a Python backend and a React frontend.
- **Performance Optimization**: Use of `useRef` and `useCallback` to handle high-frequency data updates without UI lag.
- **Clean Architecture**: Separation of concerns between the trading engine, persistence layer, and UI components.
- **State Management**: Efficient handling of complex, rapidly changing market and portfolio states.
