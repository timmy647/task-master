import { createRouter, createWebHistory } from 'vue-router';
import About from '../views/About';
import Home from '../views/Home';
import Login from '@/views/Login.vue';
import Register from '../views/Register';
import Profile from '../views/Profile';
import TasksTableView from '../views/TasksTableView';
import TasksListView from '../views/TasksListView';
import TasksBoardView from '../views/TasksBoardView';
import TasksChartView from '../views/TasksChartView';

const routes = [
  {
    path: '/',
    redirect: () => {
      return { path: '/login' };
    },
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  {
    path: '/tasks',
    redirect: () => {
      return { path: '/tasks/board' };
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/tasks/list',
    name: 'TasksList',
    component: TasksListView,
  },
  {
    path: '/tasks/board',
    name: 'TasksBoard',
    component: TasksBoardView,
  },
  {
    path: '/tasks/table',
    name: 'TasksTable',
    component: TasksTableView,
  },
  {
    path: '/tasks/chart',
    name: 'TasksChart',
    component: TasksChartView,
  },
  {
    path: '/user/:email',
    name: 'Profile',
    component: Profile,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

let isAuthenticated = true;

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
