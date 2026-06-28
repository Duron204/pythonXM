<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const emit = defineEmits<{
  (e: 'switch-tab'): void
}>()

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const rememberMe = ref(true)
const errorMsg = ref('')
const isLoading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) {
    errorMsg.value = '请输入用户名和密码'
    return
  }

  isLoading.value = true
  errorMsg.value = ''

  try {
    // 模拟登录（实际应调用API）
    await new Promise(resolve => setTimeout(resolve, 500))
    userStore.login({
      username: username.value,
      token: 'mock-token-' + Date.now()
    })
    router.push('/')
  } catch (e: any) {
    errorMsg.value = e.message || '登录失败'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-form">
    <div class="form-avatar">
      <div class="avatar-ring">
        <el-icon :size="36"><User /></el-icon>
      </div>
    </div>

    <div class="form-group">
      <div class="input-wrapper">
        <el-icon class="input-icon"><User /></el-icon>
        <input
          v-model="username"
          type="text"
          placeholder="用户名"
          maxlength="10"
          class="exo-input"
          @keyup.enter="handleLogin"
        />
      </div>
    </div>

    <div class="form-group">
      <div class="input-wrapper">
        <el-icon class="input-icon"><Lock /></el-icon>
        <input
          v-model="password"
          type="password"
          placeholder="密码"
          maxlength="12"
          class="exo-input"
          @keyup.enter="handleLogin"
        />
      </div>
    </div>

    <div class="form-options">
      <label class="checkbox-wrapper">
        <input type="checkbox" v-model="rememberMe" />
        <span class="checkbox-custom"></span>
        <span class="checkbox-label">记住密码</span>
      </label>
      <a class="link-btn" href="#">忘记密码</a>
    </div>

    <div class="error-msg" v-if="errorMsg">
      <el-icon><WarningFilled /></el-icon>
      {{ errorMsg }}
    </div>

    <button
      class="btn-exo btn-primary-exo login-btn"
      @click="handleLogin"
      :disabled="isLoading"
    >
      {{ isLoading ? '登录中...' : '登 录' }}
    </button>

    <div class="form-footer">
      <span class="footer-text">还没有账号？</span>
      <a class="link-btn" @click="emit('switch-tab')">注册账号</a>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px 0;
}

.form-avatar {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.avatar-ring {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
  transition: all 0.3s ease;

  &:hover {
    border-color: #4caf50;
    color: #4caf50;
  }
}

.form-group {
  width: 100%;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f1f8e9;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 0 16px;
  transition: all 0.2s ease;

  &:focus-within {
    border-color: #4caf50;
    background: white;
    box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.15);
  }
}

.input-icon {
  color: #ccc;
  font-size: 18px;
  margin-right: 12px;
}

.exo-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #1a1a1a;
  font-size: 14px;
  padding: 14px 0;

  &::placeholder {
    color: #ccc;
  }
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;

  input[type="checkbox"] {
    display: none;
  }

  .checkbox-custom {
    width: 18px;
    height: 18px;
    border: 2px solid #c8e6c9;
    border-radius: 4px;
    position: relative;
    transition: all 0.2s ease;
  }

  input:checked + .checkbox-custom {
    background: #4caf50;
    border-color: #4caf50;

    &::after {
      content: '';
      position: absolute;
      top: 2px;
      left: 5px;
      width: 4px;
      height: 8px;
      border: solid white;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
    }
  }

  .checkbox-label {
    color: #999;
    font-size: 13px;
    letter-spacing: 1px;
  }
}

.link-btn {
  color: #4caf50;
  font-size: 13px;
  text-decoration: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;

  &:hover {
    color: #388e3c;
  }
}

.error-msg {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #e53935;
  font-size: 13px;
}

.login-btn {
  width: 100%;
  padding: 14px;
  font-size: 14px;
  margin-top: 8px;
}

.form-footer {
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 6px;

  .footer-text {
    color: #999;
    font-size: 13px;
  }
}
</style>
