import { createApp } from 'vue'
import { createChart } from 'lightweight-charts'
import './style.css'
import App from './App.vue'

window.createLightweightChart = createChart
createApp(App).mount('#app')
