import pandas as pd
import numpy as np
from datetime import date, timedelta

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """输入 OHLCV DataFrame (index=date, cols=open/high/low/close/volume)，返回带所有技术指标的 DataFrame。"""
    # 趋势类
    df['sma_20'] = df['close'].rolling(20).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    df['sma_200'] = df['close'].rolling(200).mean()
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()
    df['macd'] = df['ema_12'] - df['ema_26']
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_histogram'] = df['macd'] - df['macd_signal']

    # ADX
    high, low, close = df['high'], df['low'], df['close']
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/14).mean()
    up = high.diff()
    down = -low.diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0), index=df.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0), index=df.index)
    plus_di = 100 * (plus_dm.ewm(alpha=1/14).mean() / atr)
    minus_di = 100 * (minus_dm.ewm(alpha=1/14).mean() / atr)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 0.0001)
    df['adx'] = dx.ewm(alpha=1/14).mean()
    df['plus_di'] = plus_di
    df['minus_di'] = minus_di

    # RSI
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1/14).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1/14).mean()
    rs = gain / (loss + 0.0001)
    df['rsi'] = 100 - (100 / (1 + rs))

    # Stochastic
    low_14 = low.rolling(14).min()
    high_14 = high.rolling(14).max()
    df['stochastic_k'] = 100 * (close - low_14) / (high_14 - low_14 + 0.0001)
    df['stochastic_d'] = df['stochastic_k'].rolling(3).mean()

    # CCI
    tp = (high + low + close) / 3
    ma = tp.rolling(20).mean()
    md = tp.rolling(20).apply(lambda x: abs(x - x.mean()).mean())
    df['cci'] = (tp - ma) / (0.015 * md + 0.0001)

    # OBV
    df['obv'] = (np.sign(close.diff()) * df['volume']).fillna(0).cumsum()

    # MFI
    typical_price = (high + low + close) / 3
    money_flow = typical_price * df['volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(), 0).rolling(14).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(), 0).rolling(14).sum()
    mfr = positive_flow / (negative_flow + 0.0001)
    df['mfi'] = 100 - (100 / (1 + mfr))

    # Volume SMA
    df['volume_sma_20'] = df['volume'].rolling(20).mean()

    # Bollinger Bands
    df['bb_middle'] = df['close'].rolling(20).mean()
    bb_std = df['close'].rolling(20).std()
    df['bb_upper'] = df['bb_middle'] + 2 * bb_std
    df['bb_lower'] = df['bb_middle'] - 2 * bb_std

    # ATR (14-period)
    df['atr'] = atr

    # Keltner Channels
    kc_mid = df['close'].ewm(span=20).mean()
    kc_atr = pd.Series(atr).ewm(span=20).mean()
    df['kc_upper'] = kc_mid + 2 * kc_atr
    df['kc_lower'] = kc_mid - 2 * kc_atr

    return df.round(4)


def generate_technical_signals(latest: dict | None) -> list[dict]:
    """从最新一行指标数据生成技术信号列表"""
    if latest is None:
        return []
    signals = []
    close = latest.get('close', 0)
    sma_50 = latest.get('sma_50')
    sma_200 = latest.get('sma_200')
    macd = latest.get('macd')
    macd_signal = latest.get('macd_signal')
    rsi = latest.get('rsi')
    volume = latest.get('volume', 0)
    volume_sma20 = latest.get('volume_sma_20')
    adx = latest.get('adx')
    plus_di = latest.get('plus_di')
    minus_di = latest.get('minus_di')
    bb_upper = latest.get('bb_upper')
    bb_lower = latest.get('bb_lower')

    if sma_50 and sma_200:
        signals.append({"indicator": "SMA 50/200", "signal": "bullish" if sma_50 > sma_200 else "bearish",
                       "value": None, "description": "金叉(看多)" if sma_50 > sma_200 else "死叉(看空)"})
    if sma_200 and close:
        signals.append({"indicator": "Price vs SMA200", "signal": "bullish" if close > sma_200 else "bearish",
                       "value": None, "description": f"价格{'高于' if close > sma_200 else '低于'}200日均线"})

    if macd and macd_signal:
        bull = macd > macd_signal
        signals.append({"indicator": "MACD", "signal": "bullish" if bull else "bearish",
                       "value": round(macd, 2), "description": f"MACD{'金叉' if bull else '死叉'}"})

    if rsi:
        sig = "bullish" if 40 <= rsi <= 65 else "bearish" if rsi > 70 else "neutral"
        desc = "中性区间" if 40 <= rsi <= 65 else "超买" if rsi > 70 else "超卖" if rsi < 30 else "正常"
        signals.append({"indicator": "RSI(14)", "signal": sig, "value": round(rsi, 2), "description": f"RSI={rsi:.1f}, {desc}"})

    if volume and volume_sma20:
        ratio = volume / (volume_sma20 + 1)
        sig = "bullish" if ratio > 1.2 else "bearish" if ratio < 0.5 else "neutral"
        signals.append({"indicator": "Volume", "signal": sig, "value": round(ratio, 2),
                       "description": f"量比={ratio:.1f}x"})

    if adx and plus_di and minus_di:
        if adx > 25:
            sig = "bullish" if plus_di > minus_di else "bearish"
            desc = f"趋势强劲, ADX={adx:.1f}"
        else:
            sig = "neutral"
            desc = f"震荡/无趋势, ADX={adx:.1f}"
        signals.append({"indicator": "ADX(14)", "signal": sig, "value": round(adx, 1), "description": desc})

    if bb_upper and bb_lower and close:
        if close < bb_lower * 1.02:
            sig = "bullish"
            desc = "触及下轨, 可能反弹"
        elif close > bb_upper * 0.98:
            sig = "bearish"
            desc = "触及上轨, 可能回调"
        else:
            sig = "neutral"
            desc = "轨道内运行"
        signals.append({"indicator": "Bollinger Bands", "signal": sig, "value": None, "description": desc})

    return signals
