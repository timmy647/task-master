<template>
  <div>
    <div class="header">
      <img src="../assets/logo.png" alt="logo" href="/" class="logo" />
      <div v-show="show_button" class="header-right">
        <router-link to="/home"><i class="fa-regular fa-bell"></i></router-link>
        <i
          class="fa-solid fa-user-plus"
          v-on:click="$emit('toggle-connection-sidebar')"
        ></i>
        <i
          style="font-size: 33px"
          class="fa-regular fa-circle-user"
          v-on:click="toggleMenu()"
          aria-haspopup="true"
          aria-controls="overlay_menu"
        ></i>
      </div>
    </div>
    <Menu
      class="dropdown"
      ref="menu"
      id="overlay_menu"
      :model="items"
      :popup="menu"
      style="position: fixed; z-index: 3; top: 80px; right: 0"
    />
  </div>
</template>

<script>
import { authLogout } from '@/service/HttpService';

export default {
  name: 'Header',
  props: {
    title: {
      type: String,
      default: 'Hello Wolrd',
    },
    show_button: {
      type: Boolean,
      default: false,
    },
    showAddTask: Boolean,
  },
  components: {},
  computed: {
    homePage() {
      if (this.$route.path === '/') {
        return true;
      } else {
        return false;
      }
    },
  },
  data() {
    return {
      menu: true,
      token: localStorage.getItem('token'),
      items: [
        {
          label: 'Profile',
          icon: 'pi pi-fw pi-user',
          command: () => {
            const email = localStorage.getItem('email');
            this.$router.push(`/user/${email}`);
            this.menu = true;
          },
        },
        {
          label: 'Sign Out',
          icon: 'pi pi-sign-out',
          command: () => {
            localStorage.removeItem('token');
            authLogout(this.token).catch((err) => {
              console.log(err);
            });
            this.$router.push('/login');
            this.menu = true;
          },
        },
      ],
    };
  },
  methods: {
    toggleMenu() {
      console.log('toggle');
      this.menu = !this.menu;
    },
  },
};
</script>

<style scoped>
@import '../styles/constant.css';
/* Style the header with a grey background and some padding */
.header {
  overflow: hidden;
  background-color: var(--backgroundColor);
  display: flex;
  justify-content: space-between;
  position: fixed;
  top: 0;
  z-index: 2;
  width: 100%;
  padding-right: 20px;
  border-bottom: inset;
}

.header img {
  height: 100px;
  padding: 12px;
}

/* Style the header links */
.header i {
  /* float: left; */
  color: var(--fontColor);
  text-align: center;
  padding: 12px;
  text-decoration: none;
  font-size: 20px;
  line-height: 25px;
  border-radius: 4px;
}

/* Change the background color on mouse-over */
.header i:hover {
  background-color: var(--hoverColor);
  color: var(--fontColor);
  cursor: pointer;
}

/* Float the link section to the right */
.header-right {
  display: flex;
  align-items: center;
}

/* Add media queries for responsiveness - when the screen is 500px wide or less, stack the links on top of each other */
@media screen and (max-width: 500px) {
  .header a {
    float: none;
    display: block;
    text-align: left;
  }
  .header-right {
    float: none;
  }
}
</style>
