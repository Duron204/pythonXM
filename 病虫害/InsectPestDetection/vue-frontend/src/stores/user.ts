import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const isLoggedIn = ref<boolean>(false)
  const username = ref<string>('')
  const avatar = ref<string>('')
  const token = ref<string>('')

  function login(data: { username: string; token: string; avatar?: string }) {
    isLoggedIn.value = true
    username.value = data.username
    token.value = data.token
    avatar.value = data.avatar || ''
    localStorage.setItem('token', data.token)
    localStorage.setItem('username', data.username)
  }

  function logout() {
    isLoggedIn.value = false
    username.value = ''
    token.value = ''
    avatar.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  function initFromStorage() {
    const savedToken = localStorage.getItem('token')
    const savedUsername = localStorage.getItem('username')
    if (savedToken && savedUsername) {
      isLoggedIn.value = true
      token.value = savedToken
      username.value = savedUsername
    }
  }

  return { isLoggedIn, username, avatar, token, login, logout, initFromStorage }
})
