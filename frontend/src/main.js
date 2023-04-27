import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import './assets/style.css'

//axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

window.axios = axios;
window.axios.defaults.baseURL = 'http://127.0.0.1:5173';
//window.axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
//window.axios.defaults.headers.get['Access-Control-Allow-Origin'] = '*';
//window.axios.defaults.withCredentials = false;

const app = createApp(App)

app.use(router)

app.mount('#app')
