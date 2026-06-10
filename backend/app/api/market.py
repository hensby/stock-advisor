from fastapi import APIRouter
import yfinance as yf

router = APIRouter(prefix="/market", tags=["market"])

INDEX_MAP = {
    "sp500": "^GSPC",
    "nasdaq": "^IXIC",
    "dow": "^DJI",
    "vix": "^VIX",
}

@router.get("/indices")
async def get_indices():
    """Fetch real market indices via yfinance, fallback to defaults."""
    result = {}
    for key, symbol in INDEX_MAP.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                prev = float(hist['Close'].iloc[-2])
                curr = float(hist['Close'].iloc[-1])
                change = round(curr - prev, 2)
                change_pct = round(change / prev * 100, 2) if prev else 0
                result[key] = {"value": curr, "change": change, "change_pct": change_pct}
            else:
                result[key] = _default(key)
        except Exception:
            result[key] = _default(key)
    return result

def _default(key: str) -> dict:
    defaults = {
        "sp500":  {"value": 5234.0, "change": 0, "change_pct": 0},
        "nasdaq": {"value": 18432.0, "change": 0, "change_pct": 0},
        "dow":    {"value": 38291.0, "change": 0, "change_pct": 0},
        "vix":    {"value": 14.2,   "change": 0, "change_pct": 0},
    }
    return defaults.get(key, {"value": 0, "change": 0, "change_pct": 0})
