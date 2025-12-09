<template>
  <div class="register-container">
    <div class="register-content">
      <!-- Left Side: Image and Branding -->
      <div class="register-left">
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

      <!-- Right Side: Register Form -->
      <div class="register-right">
        <div class="register-form-container">
          <div class="form-header">
            <h2 class="form-title">创建新账户</h2>
            <p class="form-subtitle">填写以下信息以注册新账户</p>
          </div>

          <a-form
            :model="formState"
            name="register"
            autocomplete="off"
            @finish="onFinish"
            @finishFailed="onFinishFailed"
            layout="vertical"
          >
            <a-form-item
              label="用户名"
              name="username"
              :rules="[
                { required: true, message: '请输入用户名!' },
                { min: 3, message: '用户名至少3个字符!' }
              ]"
            >
              <a-input v-model:value="formState.username" placeholder="请输入用户名" size="large" />
            </a-form-item>

            <a-form-item
              label="密码"
              name="password"
              :rules="[
                { required: true, message: '请输入密码!' },
                { min: 6, message: '密码至少6个字符!' }
              ]"
            >
              <a-input-password v-model:value="formState.password" placeholder="请输入密码" size="large" />
            </a-form-item>

            <a-form-item
              label="确认密码"
              name="confirmPassword"
              :rules="[
                { required: true, message: '请确认密码!' },
                { validator: validateConfirmPassword }
              ]"
            >
              <a-input-password v-model:value="formState.confirmPassword" placeholder="请再次输入密码" size="large" />
            </a-form-item>

            <a-form-item
              label="真实姓名"
              name="realName"
            >
              <a-input v-model:value="formState.realName" placeholder="请输入真实姓名（可选）" size="large" />
            </a-form-item>

            <a-form-item
              label="邮箱"
              name="email"
              :rules="[
                { type: 'email', message: '请输入有效的邮箱地址!' }
              ]"
            >
              <a-input v-model:value="formState.email" placeholder="your.email@company.com" size="large" />
            </a-form-item>

            <a-form-item
              label="手机号"
              name="phone"
            >
              <a-input v-model:value="formState.phone" placeholder="请输入手机号（可选）" size="large" />
            </a-form-item>

            <a-form-item>
              <a-button type="primary" html-type="submit" block size="large" class="register-button" :loading="loading">
                注册账户
              </a-button>
            </a-form-item>
          </a-form>

          <div class="register-footer">
            <p>已有账户? <a @click="goToLogin">立即登录</a></p>
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
import { register } from '@/api/auth';

const router = useRouter();
const loading = ref(false);

const formState = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  realName: '',
  email: '',
  phone: '',
});

const validateConfirmPassword = async (_rule, value) => {
  if (!value) {
    return Promise.reject('请确认密码');
  }
  if (value !== formState.password) {
    return Promise.reject('两次输入的密码不一致');
  }
  return Promise.resolve();
};

const onFinish = async (values) => {
  loading.value = true;
  try {
    const { confirmPassword, ...registerData } = values;
    const response = await register(registerData);
    
    if (response.code === 200) {
      message.success('注册成功！请登录');
      router.push('/login');
    } else {
      message.error(response.message || '注册失败');
    }
  } catch (error) {
    message.error(error.response?.data?.detail || '注册失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.register-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #f0f2f5;
}

.register-content {
  display: flex;
  height: 100%;
}

.register-left {
  flex: 1;
  background-image: url('/images/modern-shipping-port-with-containers-and-cranes-at.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  flex-direction: column;
}

.register-left::before {
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

.register-right {
  flex: 1;
  max-width: 600px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  overflow-y: auto;
}

.register-form-container {
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

.register-button {
  background: #0d3f66;
  border-color: #0d3f66;
  height: 48px;
  font-size: 16px;
  margin-top: 12px;
}

.register-button:hover {
  background: #104a7a;
  border-color: #104a7a;
}

.register-footer {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 24px;
}

.register-footer a {
  color: #1890ff;
  cursor: pointer;
}

.register-footer a:hover {
  text-decoration: underline;
}

.copyright {
  margin-top: 12px;
  color: #999;
  font-size: 12px;
}

@media (max-width: 992px) {
  .register-left {
    display: none;
  }
  
  .register-right {
    max-width: 100%;
  }
}
</style>

