import fakeredis
import json
import logging

logger = logging.getLogger(__name__)

# Using fakeredis for local development to avoid external dependencies
# In a real production app, you would use redis.Redis(host='localhost', port=6379)
r = fakeredis.FakeStrictRedis(decode_responses=True)

# Initial setup for dummy user
def init_db():
    if not r.exists("portfolio:user1"):
        logger.info("Initializing dummy portfolio for user1")
        initial_portfolio = {
            "balance_usd": 10000.0,
            "assets": {
                "BTC": 0.0,
                "ETH": 0.0
            }
        }
        r.set("portfolio:user1", json.dumps(initial_portfolio))
        r.set("trades:user1", json.dumps([]))
        r.set("bots:user1", json.dumps([]))

def get_portfolio(user_id="user1"):
    data = r.get(f"portfolio:{user_id}")
    return json.loads(data) if data else None

def update_portfolio(portfolio, user_id="user1"):
    r.set(f"portfolio:{user_id}", json.dumps(portfolio))

def get_trades(user_id="user1"):
    data = r.get(f"trades:{user_id}")
    return json.loads(data) if data else []

def add_trade(trade, user_id="user1"):
    trades = get_trades(user_id)
    trades.insert(0, trade) # Add to beginning
    r.set(f"trades:{user_id}", json.dumps(trades[:50])) # Keep last 50

def get_bots(user_id="user1"):
    data = r.get(f"bots:{user_id}")
    return json.loads(data) if data else []

def save_bots(bots, user_id="user1"):
    r.set(f"bots:{user_id}", json.dumps(bots))
