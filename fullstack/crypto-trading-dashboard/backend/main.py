import asyncio
import json
import logging
import time
from typing import List, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import websockets
from pydantic import BaseModel
from database import init_db, get_portfolio, get_bots, save_bots, get_trades, add_trade, update_portfolio

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ANTIGRAVITY Trading Engine")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State management
class MarketState:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.current_price: float = 0.0
        self.last_update: float = 0.0

state = MarketState()
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

async def broadcast_market_data(data: dict):
    """Broadcast market updates to all connected clients."""
    if not state.active_connections:
        return
        
    disconnected_clients = []
    for connection in state.active_connections:
        try:
            await connection.send_json(data)
        except Exception:
            disconnected_clients.append(connection)
            
    for client in disconnected_clients:
        if client in state.active_connections:
            state.active_connections.remove(client)

async def connect_to_binance():
    """Connect to Binance WebSocket and stream data."""
    while True:
        try:
            async with websockets.connect(BINANCE_WS_URL) as ws:
                logger.info("Successfully connected to Binance Market Stream")
                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    
                    if 'k' in data:
                        kline = data['k']
                        formatted_data = {
                            "time": int(kline['t']) / 1000,
                            "open": float(kline['o']),
                            "high": float(kline['h']),
                            "low": float(kline['l']),
                            "close": float(kline['c']),
                            "volume": float(kline['v']),
                            "is_closed": kline['x']
                        }
                        
                        state.current_price = formatted_data["close"]
                        state.last_update = time.time()
                        
                        # Trigger bot execution logic
                        await check_bots(state.current_price)
                        
                        # Broadcast to frontend
                        await broadcast_market_data(formatted_data)
                                
        except Exception as e:
            logger.error(f"Binance Stream Error: {e}")
            await asyncio.sleep(5) # Backoff before reconnect

class TradeRequest(BaseModel):
    type: str # 'buy' or 'sell'
    symbol: str
    amount: float
    price: float

@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(connect_to_binance())

@app.get("/")
def read_root():
    return {"status": "active", "engine": "ANTIGRAVITY-V1", "market": "BTC/USDT"}

@app.get("/api/portfolio")
async def api_get_portfolio():
    return get_portfolio()

@app.get("/api/trades")
async def api_get_trades():
    return get_trades()

@app.get("/api/bots")
async def api_get_bots():
    return get_bots()

@app.post("/api/bots")
async def api_save_bots(bots: list):
    save_bots(bots)
    return {"status": "success"}

@app.get("/api/market-depth")
async def get_market_depth():
    """Generate simulated market depth based on current price."""
    price = state.current_price or 60000.0 # Fallback
    
    def gen_levels(base, step_pct, side):
        levels = []
        cum_vol = 0
        for i in range(1, 15):
            p = base * (1 + (i * step_pct)) if side == "ask" else base * (1 - (i * step_pct))
            vol = (15 - i) * 0.5 * (0.5 + 0.5 * (time.time() % 1)) # Add some variance
            cum_vol += vol
            levels.append({"price": round(p, 2), "amount": round(vol, 4), "total": round(cum_vol, 4)})
        return levels

    return {
        "asks": gen_levels(price, 0.0001, "ask")[::-1],
        "bids": gen_levels(price, 0.0001, "bid"),
        "price": price
    }

@app.post("/api/trade")
async def execute_trade(trade: TradeRequest):
    portfolio = get_portfolio()
    if not portfolio:
        return {"status": "error", "message": "Critical Error: Portfolio mapping failed"}
    
    if trade.type == "buy":
        cost = trade.amount * trade.price
        if portfolio["balance_usd"] < cost:
            return {"status": "error", "message": "Insufficient USD Liquidity"}
        
        portfolio["balance_usd"] -= cost
        portfolio["assets"][trade.symbol] = portfolio["assets"].get(trade.symbol, 0) + trade.amount
    elif trade.type == "sell":
        if portfolio["assets"].get(trade.symbol, 0) < trade.amount:
            return {"status": "error", "message": f"Insufficient {trade.symbol} holdings"}
        
        portfolio["assets"][trade.symbol] -= trade.amount
        portfolio["balance_usd"] += trade.amount * trade.price
    else:
        return {"status": "error", "message": "Invalid execution type"}
    
    update_portfolio(portfolio)
    
    new_trade = {
        "type": trade.type,
        "symbol": trade.symbol,
        "amount": trade.amount,
        "price": trade.price,
        "timestamp": time.time()
    }
    add_trade(new_trade)
    
    return {"status": "success", "portfolio": portfolio}

async def check_bots(price: float):
    """Check all active bots and execute trades if triggers are met."""
    bots = get_bots()
    portfolio = get_portfolio()
    if not bots or not portfolio:
        return

    updated_bots = []
    bots_changed = False
    
    for bot in bots:
        if bot.get("status") != "active":
            updated_bots.append(bot)
            continue
            
        trigger_price = float(bot["trigger_price"])
        action = bot["action"]
        amount = float(bot["amount"])
        symbol = bot["symbol"]
        
        executed = False
        if action == "buy" and price <= trigger_price:
            cost = amount * price
            if portfolio["balance_usd"] >= cost:
                portfolio["balance_usd"] -= cost
                portfolio["assets"][symbol] = portfolio["assets"].get(symbol, 0) + amount
                executed = True
        elif action == "sell" and price >= trigger_price:
            if portfolio["assets"].get(symbol, 0) >= amount:
                portfolio["assets"][symbol] -= amount
                portfolio["balance_usd"] += amount * price
                executed = True
                
        if executed:
            logger.info(f"STRATEGY TRIGGERED: Bot {bot['name']} executed {action} for {amount} {symbol} at ${price}")
            new_trade = {
                "type": action,
                "symbol": symbol,
                "amount": amount,
                "price": price,
                "timestamp": time.time(),
                "bot_id": bot.get("id")
            }
            add_trade(new_trade)
            bot["status"] = "completed"
            bots_changed = True
        
        updated_bots.append(bot)
        
    if bots_changed:
        update_portfolio(portfolio)
        save_bots(updated_bots)

@app.websocket("/ws/market")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state.active_connections.append(websocket)
    try:
        while True:
            # Keep connection alive and listen for pings/messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in state.active_connections:
            state.active_connections.remove(websocket)
        logger.info("Client session terminated")
