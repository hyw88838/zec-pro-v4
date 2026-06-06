from __future__ import annotations

import os
from typing import List, Dict

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .quant import analyze

app = FastAPI(title="ZEC-PRO V4 Enterprise")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

OKX = "https://www.okx.com"


class TradeRequest(BaseModel):
    symbol: str = "ZEC-USDT"
    side: str
    amount: float


@app.get("/health")
def health():
    return {"status": "ok", "app": os.getenv("APP_NAME", "ZEC-PRO V4 Enterprise")}


async def okx_candles(symbol: str, bar: str, limit: int = 180) -> List[Dict]:
    url = f"{OKX}/api/v5/market/history-candles"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params={"instId": symbol, "bar": bar, "limit": str(limit)})
    data = r.json()
    if data.get("code") != "0":
        raise HTTPException(502, data)
    candles = []
    for k in reversed(data["data"]):
        candles.append({
            "ts": int(k[0]), "open": float(k[1]), "high": float(k[2]),
            "low": float(k[3]), "close": float(k[4]), "volume": float(k[5])
        })
    return candles


@app.get("/api/market/snapshot")
async def snapshot(symbol: str = "ZEC-USDT", bar: str = "1H"):
    candles = await okx_candles(symbol, bar)
    q = analyze(candles)
    return {"symbol": symbol, "bar": bar, "candles": candles[-120:], "quant": q}


@app.post("/api/trade/paper")
def paper_trade(req: TradeRequest):
    return {"mode": "paper", "accepted": True, "order": req.model_dump()}


@app.post("/api/trade/live")
def live_trade(req: TradeRequest):
    if os.getenv("LIVE_TRADING", "false").lower() != "true":
        raise HTTPException(403, "LIVE_TRADING=false，真实交易安全锁未开启")
    return {"mode": "live", "accepted": False, "message": "实盘适配器未启用"}
