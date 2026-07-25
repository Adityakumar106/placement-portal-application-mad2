import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/index.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.config.globalProperties.$apiBase = `${window.location.protocol}//${window.location.hostname}:5000`

app.use(router).mount('#app')
