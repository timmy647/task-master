<template>
  <div class="container">
    <div class="login-form">
      <h1 class="p-text-center p-mb-2">Login</h1>
      <form @submit.prevent="submit">
        <div class="p-field p-mb-5">
          <label for="username" class="form-label">Username</label>
          <div>
            <input
              id="username"
              type="text"
              v-model.trim="username"
              class="p-inputtext p-component p-filled"
              maxlength="20"
            />
            <div v-if="username.length === 20" class="p-error">
              Username must be under 20 characters.
            </div>
          </div>
        </div>
        <div class="p-field p-mb-5">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            type="password"
            v-model.trim="password"
            class="p-inputtext p-component p-filled"
          />
        </div>
        <div class="p-field">
          <button
            type="submit"
            class="login-btn"
            :disabled="username.length > 20"
          >
            Login
          </button>
          <button
            type="button"
            class="register-btn"
            @click="navigateToRegister"
          >
            Register
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { authLogin } from '../service/HttpService';
export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async submit() {
      if (this.username.length <= 20) {
        try {
          const res = await authLogin(this.username, this.password);
          await localStorage.setItem('token', res.token);
          await localStorage.setItem('email', this.username);
          await this.$router.push('/home');
        } catch (err) {
          alert(err);
        }
      }
    },
    navigateToRegister() {
      this.$router.push('/register'); // Redirect to the register page
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 75vh;
}

.login-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-width: 600px;
  padding: 40px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.p-text-center {
  margin-bottom: 2rem;
}

.form-label {
  margin-bottom: 20px;
  font-size: 1.4em;
}

.p-inputtext {
  font-size: 1.3em;
  padding: 15px;
  margin-left: 20px;
  margin-right: 30px;
  width: auto;
}

.p-field {
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center; /* aligned to center */
}

.p-error {
  color: red;
  margin-top: 5px;
}

.login-btn,
.register-btn {
  width: 120px;
  margin: 10px;
  padding: 15px 25px;
  background-color: #4caf50;
  border: none;
  color: white;
  text-align: center;
  display: inline-block;
  font-size: 20px;
  transition-duration: 0.4s;
  cursor: pointer;
  border-radius: 12px;
}

.login-btn:hover,
.register-btn:hover {
  background-color: #45a049;
}
</style>
