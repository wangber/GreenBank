import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false
App.mpType = 'app'

const app = new Vue(App)
app.$mount()
import 'mpvue-weui/src/style/weui.css';
export default {
    config: {
        pages: [
            'pages/index/main',
            'pages/second/main'
        ]
    }
}