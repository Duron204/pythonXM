<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'switch-tab'): void
}>()

const username = ref('')
const password = ref('')
const captcha = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
const captchaCode = ref('')

function generateCaptcha() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789'
  let code = ''
  for (let i = 0; i < 4; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  captchaCode.value = code
}

generateCaptcha()

async function handleRegister() {
  if (!username.value || !password.value || !captcha.value) {
    errorMsg.value = '请填写所有字段'
    return
  }

  if (captcha.value !== captchaCode.value) {
    errorMsg.value = '验证码错误'
    generateCaptcha()
    return
  }

  isLoading.value = true
  errorMsg.value = ''

  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    alert('注册成功！')
    emit('switch-tab')
  } catch (e: any) {
    errorMsg.value = e.message || '注册失败'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="register-form">
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
        />
      </div>
    </div>

    <div class="form-group captcha-group">
      <div class="input-wrapper">
        <el-icon class="input-icon"><Key /></el-icon>
        <input
          v-model="captcha"
          type="text"
          placeholder="验证码"
          maxlength="4"
          class="exo-input"
          @keyup.enter="handleRegister"
        />
      </div>
      <div class="captcha-display" @click="generateCaptcha" title="点击刷新">
        <canvas ref="captchaCanvas" width="100" height="36" id="captchaCanvas"></canvas>
        <span class="captcha-code">{{ captchaCode }}</span>
      </div>
    </div>

    <div class="error-msg" v-if="errorMsg">
      <el-icon><WarningFilled /></el-icon>
      {{ errorMsg }}
    </div>

    <button
      class="btn-exo btn-primary-exo register-btn"
      @click="handleRegister"
      :disabled="isLoading"
    >
      {{ isLoading ? '注册中...' : '注 册' }}
    </button>

    <div class="form-footer">
      <span class="footer-text">已有账号？</span>
      <a class="link-btn" @click="emit('switch-tab')">前往登录</a>
    </div>
  </div>
</template>

<style scoped lang="scss">
.register-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px 0;
}

.form-avatar {
  display: flex;
  justify-content: center;
  margin-bottom: 4px;
}

.avatar-ring {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid #c8e6c9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8aa67a;
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
  color: #8aa67a;
  font-size: 18px;
  margin-right: 12px;
}

.exo-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #2e3d27;
  font-size: 14px;
  padding: 14px 0;

  &::placeholder {
    color: #c8e6c9;
  }
}

.captcha-group {
  display: flex;
  gap: 10px;

  .input-wrapper {
    flex: 1;
  }
}

.captcha-display {
  width: 100px;
  height: 40px;
  background: #f1f8e9;
  border: 2px solid #c8e6c9;
  border-radius: 10px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover {
    border-color: #4caf50;
    box-shadow: 0 0 10px rgba(76, 175, 80, 0.2);
  }

  .captcha-code {
    color: #388e3c;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 6px;
    font-family: 'Courier New', monospace;
  }
}

.error-msg {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #e53935;
  font-size: 13px;
}

.register-btn {
  width: 100%;
  padding: 14px;
  font-size: 14px;
  margin-top: 4px;
}

.form-footer {
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 6px;

  .footer-text {
    color: #8aa67a;
    font-size: 13px;
  }
}

.link-btn {
  color: #4caf50;
  font-size: 13px;
  text-decoration: none;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.2s ease;

  &:hover {
    text-shadow: 0 0 8px rgba(57, 255, 20, 0.5);
  }
}
</style>
