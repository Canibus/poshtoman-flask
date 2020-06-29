import Vue from 'vue'
import Router from 'vue-router'
import store from './store.js'

Vue.use(Router)

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isLoggedIn) {
    next()
    return
  }
  next('/login')
}

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () => import('@/views/dashboard/Index'),
      beforeEnter: ifAuthenticated,
      children: [
        // Dashboard
        {
          name: 'Dashboard',
          path: '',
          component: () => import('@/views/dashboard/Dashboard'),
        },
        // Pages
        {
          name: 'User Profile',
          path: 'pages/user',
          component: () => import('@/views/dashboard/pages/UserProfile'),
        },
        {
          name: 'Notifications',
          path: 'components/notifications',
          component: () => import('@/views/dashboard/component/Notifications'),
        },
        {
          name: 'Users',
          path: 'tables/users',
          component: () => import('@/views/dashboard/tables/Users'),
        },
        {
          name: 'Places',
          path: 'tables/places',
          component: () => import('@/views/dashboard/tables/Places'),
        },
        {
          name: 'Pms',
          path: 'tables/pms',
          component: () => import('@/views/dashboard/tables/Pms'),
        },
        // Maps
        {
          name: 'Google Maps',
          path: 'maps/maps',
          component: () => import('@/views/dashboard/maps/Maps'),
        },
      ],
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/login',
      component: () => import('@/views/dashboard/pages/LoginPage'),
    },
  ],
})
