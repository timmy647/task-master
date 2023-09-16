<template>
  <div class="container">
    <div class="register-form">
      <h1 class="p-text-center p-mb-4">Register</h1>
      <form @submit.prevent="submit">
        <!-- Username field -->
        <div class="p-field p-mb-5">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            type="text"
            v-model.trim="username"
            class="p-inputtext p-component p-filled"
            maxlength="20"
          />
          <div v-if="username.length > 20" class="p-error">
            Username must be under 20 characters.
          </div>
        </div>
        <!-- Email field -->
        <div class="p-field p-mb-5">
          <label for="email" class="form-label">Email Address</label>
          <input
            id="email"
            type="email"
            v-model.trim="email"
            class="p-inputtext p-component p-filled"
          />
          <div v-if="!isValidEmail && email.length > 0" class="p-error">
            Please enter a valid email address.
          </div>
        </div>
        <!-- Password field -->
        <div class="p-field p-mb-5">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            type="password"
            v-model.trim="password"
            class="p-inputtext p-component p-filled"
          />
          <!-- <div v-if="!isValidPassword && password.length > 0" class="p-error">
            Password must be at least 8 characters long and contain at least one
            lowercase letter, one uppercase letter, one digit, and one special
            character.
          </div> -->
        </div>
        <!-- Submit button -->
        <div class="p-field">
          <button
            type="submit"
            class="p-button p-component p-button-success p-button-lg p-button-block register-btn"
            :disabled="false"
          >
            Register
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { authRegister } from '../service/HttpService';
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
    };
  },
  computed: {
    isValidEmail() {
      // Regular expression to validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(this.email);
    },
    isValidPassword() {
      // Regular expression to validate password format
      const passwordRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return passwordRegex.test(this.password);
    },
    isFormValid() {
      return (
        this.username.length <= 20 && this.isValidEmail && this.isValidPassword
      );
    },
  },
  methods: {
    submit() {
      const test = true;
      if (this.isFormValid || test) {
        authRegister(this.email, this.password, this.username)
          .then((res) => {
            localStorage.setItem('token', res.token);
            localStorage.setItem('email', this.email);
            this.$router.push('/home'); // Navigate to the home page
          })
          .catch((err) => alert(err));
      } else {
        if (this.username.length > 20) {
          alert('Username must be under 20 characters.');
        }
        if (!this.isValidEmail && this.email.length > 0) {
          alert('Please enter a valid email address.');
        }
        if (!this.isValidPassword && this.password.length > 0) {
          alert(
            'Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.'
          );
        }
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px;
  height: 100vh;
}

.register-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-width: 400px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-label {
  margin-bottom: 15px;
  font-size: 1.2em;
}

.p-inputtext {
  font-size: 1.1em;
  padding: 10px;
  margin-left: 20px;
  margin-right: 20px;
}

.p-button {
  font-size: 1.1em;
  padding: 10px;
  margin-left: 20px;
  margin-right: 20px;
}

.p-field {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.register-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
