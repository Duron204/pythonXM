<script setup lang="ts">
import { ref } from 'vue'
import LoginForm from '@/components/login/LoginForm.vue'
import RegisterForm from '@/components/login/RegisterForm.vue'

const activeTab = ref<'login' | 'register'>('login')
</script>

<template>
  <div class="login-view">
    <div class="login-container">
      <!-- 左侧装饰区 -->
      <div class="login-left">
        <div class="decoration-circle large"></div>
        <div class="decoration-circle medium"></div>
        <div class="decoration-circle small"></div>

        <div class="brand-info">
          <div class="brand-icon">
            <svg viewBox="0 0 100 100" width="120" height="120">
              <circle cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="2" opacity="0.3" />
              <circle cx="50" cy="50" r="30" fill="none" stroke="white" stroke-width="1.5" opacity="0.2" />
              <circle cx="50" cy="50" r="15" fill="rgba(255,255,255,0.1)" stroke="white" stroke-width="1" opacity="0.3" />
            </svg>
          </div>
          <h2 class="brand-title">害虫检测系统</h2>
          <p class="brand-subtitle">PEST DETECTION SYSTEM</p>
        </div>
      </div>

      <!-- 右侧表单区 -->
      <div class="login-right">
        <div class="form-header">
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'login' }"
            @click="activeTab = 'login'"
          >
            <el-icon><User /></el-icon>
            <span>登录</span>
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'register' }"
            @click="activeTab = 'register'"
          >
            <el-icon><DocumentAdd /></el-icon>
            <span>注册</span>
          </button>
        </div>

        <div class="form-body">
          <Transition name="slide" mode="out-in">
            <LoginForm v-if="activeTab === 'login'" @switch-tab="activeTab = 'register'" />
            <RegisterForm v-else @switch-tab="activeTab = 'login'" />
          </Transition>
        </div>
      </div>
    </div>

    <div class="login-footer">
      <span>基于YOLOv8/v5的农作物害虫检测系统 v1.0</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-view {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #4caf50 0%, #81c784 100%);
  position: relative;
  overflow: hidden;
}

.login-container {
  display: flex;
  width: 900px;
  max-width: 95vw;
  min-height: 500px;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.1);

  &.large {
    width: 300px;
    height: 300px;
    top: -50px;
    right: -100px;
  }

  &.medium {
    width: 200px;
    height: 200px;
    bottom: -30px;
    left: -50px;
  }

  &.small {
    width: 100px;
    height: 100px;
    top: 30%;
    left: 20%;
    background: rgba(242, 101, 34, 0.1);
  }
}

.brand-info {
  text-align: center;
  z-index: 1;
}

.brand-icon {
  margin-bottom: 30px;
  animation: float 3s ease-in-out infinite;
}

.brand-title {
  font-size: 24px;
  color: white;
  letter-spacing: 4px;
  margin-bottom: 10px;
  font-weight: 700;
}

.brand-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 3px;
  text-transform: uppercase;
}

.login-right {
  width: 420px;
  display: flex;
  flex-direction: column;
}

.form-header {
  display: flex;
  border-bottom: 1px solid #e8f5e9;

  .tab-btn {
    flex: 1;
    padding: 18px;
    background: transparent;
    border: none;
    color: #999;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;

    &:hover {
      color: #666;
    }

    &.active {
      color: #4caf50;
      border-bottom: 2px solid #4caf50;
      margin-bottom: -1px;
    }
  }
}

.form-body {
  flex: 1;
  padding: 20px 32px;
  overflow-y: auto;
}

.login-footer {
  margin-top: 20px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  letter-spacing: 1px;
  z-index: 1;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
