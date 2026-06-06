<template>
  <main class="wrap">
    <header class="glass header">
      <div><h1>ZEC-PRO V4 Enterprise</h1><p>AI Quant Terminal · OKX Market · Paper Trading Safe Mode</p></div>
      <div class="controls">
        <select v-model="symbol" @change="load"><option>ZEC-USDT</option><option>BTC-USDT</option><option>ETH-USDT</option><option>SOL-USDT</option></select>
        <select v-model="bar" @change="load"><option>5m</option><option>15m</option><option>1H</option><option>4H</option><option>1D</option></select>
        <button @click="load">刷新</button>
      </div>
    </header>
    <section class="grid">
      <div class="glass card chart-card"><div id="chart"></div></div>
      <div class="glass card score"><span>AI SCORE</span><strong :class="dirClass">{{ quant.score ?? '--' }}</strong><b :class="dirClass">{{ quant.direction || 'WAIT' }}</b><p>Risk: {{ quant.risk || '--' }}</p></div>
      <div class="glass card"><h3>指标</h3><div class="row"><span>Price</span><b>${{ f(quant.price) }}</b></div><div class="row"><span>RSI</span><b>{{ quant.rsi }}</b></div><div class="row"><span>MACD</span><b>{{ quant.macd_hist }}</b></div><div class="row"><span>ATR%</span><b>{{ quant.atr_pct }}%</b></div></div>
      <div class="glass card"><h3>支撑压力</h3><div class="row" v-for="(v,k) in quant.levels" :key="k"><span>{{ k }}</span><b>{{ f(v) }}</b></div></div>
      <div class="glass card signal"><h3>交易计划</h3><p>{{ plan }}</p><button @click="paper">Paper Trade</button></div>
    </section>
  </main>
</template>
<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
const symbol=ref('ZEC-USDT'), bar=ref('1H'), quant=ref({}), candles=ref([]); let chart, series
const f=(n)=> Number.isFinite(n)?Number(n).toLocaleString('en-US',{maximumFractionDigits:4}):'--'
const dirClass=computed(()=> quant.value.direction==='LONG'?'green':quant.value.direction==='SHORT'?'red':'yellow')
const plan=computed(()=> quant.value.direction==='LONG'?'偏多：等回踩支撑，ATR止损，分批止盈。':quant.value.direction==='SHORT'?'偏空：等反弹压力，严格止损。':'震荡：等待评分突破或关键位确认。')
async function load(){ const r=await fetch(`/api/market/snapshot?symbol=${symbol.value}&bar=${bar.value}`); const j=await r.json(); quant.value=j.quant; candles.value=j.candles; await nextTick(); draw() }
function draw(){ if(!chart){ chart=window.createLightweightChart(document.getElementById('chart'),{layout:{background:{color:'transparent'},textColor:'#94a3b8'},grid:{vertLines:{color:'rgba(0,240,255,.08)'},horzLines:{color:'rgba(0,240,255,.08)'}},timeScale:{timeVisible:true}}); series=chart.addCandlestickSeries({upColor:'#00ff9d',downColor:'#ff2f5f',borderVisible:false,wickUpColor:'#00ff9d',wickDownColor:'#ff2f5f'}) } series.setData(candles.value.map(x=>({time:Math.floor(x.ts/1000),open:x.open,high:x.high,low:x.low,close:x.close}))); chart.timeScale().fitContent() }
async function paper(){ await fetch('/api/trade/paper',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({symbol:symbol.value,side:quant.value.direction,amount:1})}); alert('纸交易已记录') }
onMounted(load)
</script>
