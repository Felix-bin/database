<template>
  <div class="login-container">
    <div class="login-content">
      <!-- Left Side: Image and Branding -->
      <div class="login-left">
        <div class="brand-overlay">
          <div class="brand-header">
            <div class="logo-icon">
              <span class="icon-container"><container-outlined /></span>
            </div>
            <span class="brand-name">海洋装备管理</span>
          </div>
          
          <div class="brand-content">
            <h1 class="brand-title">智能化船舶装备<br>租赁与仓储平台</h1>
            <p class="brand-subtitle">为港口管理、设备租赁和仓储运营提供专业的数字化解决方案</p>
            
            <div class="brand-stats">
              <div class="stat-item">
                <div class="stat-value">1000+</div>
                <div class="stat-label">装备类型</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">50+</div>
                <div class="stat-label">合作港口</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">99.9%</div>
                <div class="stat-label">系统可用性</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side: Login Form -->
      <div class="login-right">
        <div class="login-form-container">
          <div class="form-header">
            <h2 class="form-title">登录您的账户</h2>
            <p class="form-subtitle">输入您的凭据以访问仓储管理系统</p>
          </div>

          <a-form
            :model="formState"
            name="basic"
            autocomplete="off"
            @finish="onFinish"
            @finishFailed="onFinishFailed"
            layout="vertical"
          >
            <a-form-item
              label="用户名或邮箱"
              name="username"
              :rules="[{ required: true, message: '请输入用户名或邮箱!' }]"
            >
              <a-input v-model:value="formState.username" placeholder="your.email@company.com" size="large" />
            </a-form-item>

            <a-form-item
              label="密码"
              name="password"
              :rules="[{ required: true, message: '请输入密码!' }]"
            >
              <div class="password-label-wrapper" slot="label">
                <span>密码</span>
                <a class="forgot-password" href="#">忘记密码?</a>
              </div>
              <a-input-password v-model:value="formState.password" placeholder="........" size="large" />
            </a-form-item>

            <a-form-item name="remember" valuePropName="checked">
              <a-checkbox v-model:checked="formState.remember">保持登录状态</a-checkbox>
            </a-form-item>

            <a-form-item>
              <a-button type="primary" html-type="submit" block size="large" class="login-button" :loading="loading">
                登录系统
              </a-button>
            </a-form-item>
          </a-form>

          <div class="login-footer">
            <p>还没有账户? <a @click="goToRegister">立即注册</a></p>
            <p>需要帮助? <a href="#">联系技术支持</a></p>
            <p class="copyright">© 2025 海洋装备管理系统 · 版本 2.0</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { ContainerOutlined } from '@ant-design/icons-vue';
import { login as loginApi } from '@/api/auth';

const router = useRouter();
const loading = ref(false);

const formState = reactive({
  username: '',
  password: '',
  remember: false,
});

const onFinish = async (values) => {
  loading.value = true;
  try {
    const response = await loginApi({
      username: values.username,
      password: values.password
    });
    
    if (response.code === 200) {
      message.success('登录成功');
      // 存储用户信息（可以后续使用 Pinia store）
      if (values.remember) {
        localStorage.setItem('userInfo', JSON.stringify(response.data));
      } else {
        sessionStorage.setItem('userInfo', JSON.stringify(response.data));
      }
      router.push('/dashboard');
    } else {
      message.error(response.message || '登录失败');
    }
  } catch (error) {
    message.error(error.response?.data?.detail || '登录失败，请检查用户名和密码');
  } finally {
    loading.value = false;
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #f0f2f5;
}

.login-content {
  display: flex;
  height: 100%;
}

.login-left {
  flex: 1;
  background-image: url('/images/modern-shipping-port-with-containers-and-cranes-at.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  flex-direction: column;
}

.login-left::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(16, 44, 87, 0.75) 0%, rgba(13, 31, 60, 0.7) 100%);
}

.brand-overlay {
  position: relative;
  z-index: 1;
  padding: 40px;
  height: 100%;
  display: flex;
  flex-direction: column;
  color: white;
}

.brand-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: auto;
}

.icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
}

.brand-name {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.brand-content {
  margin-bottom: 60px;
  padding-right: 20%;
}

.brand-title {
  font-size: 42px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 24px;
  color: white;
}

.brand-subtitle {
  font-size: 16px;
  line-height: 1.6;
  opacity: 0.85;
  margin-bottom: 48px;
}

.brand-stats {
  display: flex;
  gap: 48px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.7;
}

.login-right {
  flex: 1;
  max-width: 600px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-form-container {
  width: 100%;
  max-width: 400px;
}

.form-header {
  margin-bottom: 40px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.form-subtitle {
  color: #666;
  font-size: 14px;
}

/* Customizing Ant Design Form */
:deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: #333;
}

.password-label-wrapper {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.forgot-password {
  color: #1890ff;
  font-size: 12px;
  float: right;
}

.login-button {
  background: #0d3f66;
  border-color: #0d3f66;
  height: 48px;
  font-size: 16px;
  margin-top: 12px;
}

.login-button:hover {
  background: #104a7a;
  border-color: #104a7a;
}

.login-footer {
  text-align: center;
  color: #666;
  font-size: 14px;
}

.login-footer a {
  color: #1890ff;
  cursor: pointer;
}

.login-footer a:hover {
  text-decoration: underline;
}

.copyright {
  margin-top: 12px;
  color: #999;
  font-size: 12px;
}

@media (max-width: 992px) {
  .login-left {
    display: none;
  }
  
  .login-right {
    max-width: 100%;
  }
}
</style>

