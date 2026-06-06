from __future__ import annotations

from typing import List, Dict


def ema(values: List[float], period: int) -> List[float]:
    if not values:
        return []
    k = 2 / (period + 1)
    out, v = [], values[0]
    for x in values:
        v = x * k + v * (1 - k)
        out.append(v)
    return out


def rsi(closes: List[float], period: int = 14) -> float:
    if len(closes) <= period + 1:
        return 50.0
    gains = losses = 0.0
    for i in range(1, period + 1):
        d = closes[i] - closes[i - 1]
        gains += max(d, 0)
        losses += max(-d, 0)
    gains /= period
    losses /= period
    for i in range(period + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains = (gains * (period - 1) + max(d, 0)) / period
        losses = (losses * (period - 1) + max(-d, 0)) / period
    if losses == 0:
        return 100.0
    return 100 - 100 / (1 + gains / losses)


def atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
    if len(closes) <= period + 1:
        return 0.0
    trs = []
    for i in range(1, len(closes)):
        trs.append(max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])))
    value = sum(trs[:period]) / period
    for tr in trs[period:]:
        value = (value * (period - 1) + tr) / period
    return value


def macd_hist(closes: List[float]) -> float:
    if len(closes) < 35:
        return 0.0
    e12, e26 = ema(closes, 12), ema(closes, 26)
    macd_line = [a - b for a, b in zip(e12, e26)]
    signal = ema(macd_line, 9)
    return macd_line[-1] - signal[-1]


def analyze(candles: List[Dict]) -> Dict:
    closes = [float(x["close"]) for x in candles]
    highs = [float(x["high"]) for x in candles]
    lows = [float(x["low"]) for x in candles]
    price = closes[-1]
    r = rsi(closes)
    m = macd_hist(closes)
    a = atr(highs, lows, closes)
    e20 = ema(closes, 20)[-1]
    e50 = ema(closes, 50)[-1]
    prev = candles[-2]
    p = (prev["high"] + prev["low"] + prev["close"]) / 3
    levels = {
        "P": p,
        "R1": 2 * p - prev["low"],
        "S1": 2 * p - prev["high"],
        "R2": p + (prev["high"] - prev["low"]),
        "S2": p - (prev["high"] - prev["low"]),
    }
    score = 50
    score += 14 if price > e20 else -14
    score += 12 if e20 > e50 else -12
    score += 8 if m > 0 else -8
    score += 6 if r > 58 else -6 if r < 42 else 0
    score = max(0, min(100, round(score)))
    direction = "LONG" if score >= 68 else "SHORT" if score <= 32 else "WAIT"
    return {
        "price": price,
        "rsi": round(r, 2),
        "macd_hist": round(m, 6),
        "atr": round(a, 6),
        "atr_pct": round(a / price * 100, 3) if price else 0,
        "ema20": round(e20, 6),
        "ema50": round(e50, 6),
        "score": score,
        "direction": direction,
        "levels": {k: round(v, 6) for k, v in levels.items()},
        "risk": "HIGH" if a / price * 100 > 4 else "NORMAL",
    }
