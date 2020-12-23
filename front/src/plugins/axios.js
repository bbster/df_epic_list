import Vue from 'vue'
import Axios from 'axios';

export default Vue.install = function (Vue) {
    const instance = Axios.create({
        baseURL: 'http://localhost:8000',
        timeout: 3000,
        post: {
            "Content-Type": "application/json",
        },

    });
    Vue.prototype.$axios = {
        post: instance.post,
        get: instance.get,
    }
}