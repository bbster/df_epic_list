import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '@/pages/index';
import HelloWorldPage from '@/pages/helloWorld';
import TodoPage from '@/pages/todo';

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Home',
            component: HomePage,
        },
        {
            path: '/helloworld',
            name: 'HelloWorld',
            component: HelloWorldPage
        },
        {
            path: '/todo',
            name: 'Todo',
            component: TodoPage
        }
    ]
});