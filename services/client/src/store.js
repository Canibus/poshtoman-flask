import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import config from './config'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {},
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: 'https://demos.creative-tim.com/material-dashboard/assets/img/sidebar-1.jpg',
    drawer: null,
  },
  mutations: {
    SET_BAR_IMAGE (state, payload) {
      state.barImage = payload
    },
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
    auth_request (state) {
      state.status = 'loading'
    },
    auth_success (state, token, user) {
      state.status = 'success'
      state.token = token
      state.user = user
    },
    auth_error (state) {
      state.status = 'error'
    },
    logout (state) {
      state.status = ''
      state.token = ''
    },
  },
  actions: {
    login ({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({ url: `${config.apiUrl}/api/v2/admins/login`, data: user, method: 'POST' })
        .then(resp => {
          const token = resp.data.jwt_token
          const user = resp.data.user
          localStorage.setItem('token', token)
          axios.defaults.headers.common['api-token'] = token
          commit('auth_success', token, user)
          resolve(resp)
        })
        .catch(err => {
          commit('auth_error')
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },
    logout ({ commit }) {
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['api-token']
        resolve()
      })
    },
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
  },
})
