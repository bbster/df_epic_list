import Vue from 'vue';
import Axios from "@/plugins/axios";
import router from '@/router'
import App from './App.vue'

Vue.config.productionTip = false;

Vue.use(Axios);

new Vue({
  render: h => h(App),
  router,
}).$mount('#app')
