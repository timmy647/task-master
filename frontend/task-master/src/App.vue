<template>
  <div class="container">
    <Header
      title="Task Master"
      :showAddTask="showAddTask"
      @toggle-connection-sidebar="toggleSideBar"
      :show_button="SignedIn"
    />
    <!-- The sidebar
    <div class="sidebar" v-if="isUserAuthenticated">
      <div><router-link class="active" to="home">Home</router-link></div>
      <div><router-link to="tasks">My Tasks</router-link></div>
    </div> -->
    <router-view :key="this.$route.fullPath"></router-view>
    <DynamicDialog />
    <Sidebar v-model:visible="sidebarVisible" position="right">
      <h2>Add a Connection</h2>
      <div class="flex">
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText v-model="connectionEmail" placeholder="Search by Email" />
        </span>
        <span class="flex justify-content-end">
          <Button v-on:click="() => handleAddConnection(connectionEmail)"
            >Add</Button
          >
        </span>
      </div>
      <small id="username-help"
        >Enter your email to find a new connection.</small
      >
    </Sidebar>
  </div>
</template>

<script>
import Header from './components/Header';
import { ref } from 'vue';
import { connectionRequest } from './service/HttpService';
import DynamicDialog from 'primevue/dynamicdialog';

export default {
  name: 'App',
  components: {
    Header,
    DynamicDialog,
  },
  created() {},
  data() {
    return {
      tasks: [],
      showAddTask: false,
      isUserAuthenticated: localStorage.getItem('userAuthenticated') === 'true',
      sidebarVisible: false,
      connectionEmail: ref(''),
    };
  },
  methods: {
    async fetchTasks() {
      const res = await fetch('https://localhost:5000/tasks');
      const data = await res.json();
      return data;
    },
    toggleSideBar() {
      this.sidebarVisible = !this.sidebarVisible;
    },
    async handleAddConnection(connectionEmail) {
      try {
        const res = await connectionRequest(
          localStorage.getItem('token'),
          connectionEmail
        );
        alert(res.message);
      } catch (err) {
        alert(err);
      }
    },
  },
  computed: {
    SignedIn() {
      if (this.$route.path !== '/register' && this.$route.path !== '/login') {
        return true;
      } else {
        return false;
      }
    },
  },
  watch: {
    $route: function () {
      this.isUserAuthenticated =
        localStorage.getItem('userAuthenticated') === 'true';
    },
  },
};
</script>

<style>
@import '/node_modules/primeflex/primeflex.css';
@import './styles/constant.css';

/* The side navigation menu */
.sidebar {
  margin: 0;
  padding: 0;
  top: 120px;
  width: 200px;
  background-color: var(--backgroundColor);
  position: fixed;
  height: 87%;
  overflow: auto;
  border-right: inset;
}

/* Sidebar links */
.sidebar a {
  display: block;
  color: var(--fontColor);
  padding: 16px;
  text-decoration: none;
}

/* Active/current link */
.sidebar a.active {
  background-color: var(--activeColor);
  color: var(--backgroundColor);
}

/* Links on mouse-over */
.sidebar a:hover:not(.active) {
  background-color: var(--hoverColor);
  color: var(--fontColor);
}

/* Page content. The value of the margin-left property should match the value of the sidebar's width property */
div.content {
  margin-top: 130px;
  margin-left: 250px;
  padding: 1px 16px;
  height: 1000px;
}

/* On screens that are less than 700px wide, make the sidebar into a topbar */
@media screen and (max-width: 700px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  .sidebar a {
    float: left;
  }
  div.content {
    margin-left: 0;
  }
}

/* On screens that are less than 400px, display the bar vertically, instead of horizontally */
@media screen and (max-width: 400px) {
  .sidebar a {
    text-align: center;
    float: none;
  }
}

.clickable {
  cursor: pointer;
}

.clickable:hover {
  background-color: lightblue;
  /* text-decoration: underline; */
}
</style>
