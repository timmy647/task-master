<template>
  <div>
    <div class="sidebar">
      <div><router-link to="/home">Home</router-link></div>
      <div><router-link to="/tasks/table">My Tasks</router-link></div>
    </div>
    <div class="content">
      <div
        class="flex align-content-center flex-wrap"
        style="min-height: 100px"
      >
        <div v-if="icon_image === ''">
          <Avatar icon="pi pi-user" class="mr-2" size="xlarge" shape="circle" />
        </div>
        <div v-else>
          <Avatar :image="icon_image" shape="circle" />
        </div>
        <div class="flex flex-column">
          <span class="name">{{ name }}</span>
          <span class="email">{{ email }}</span>
        </div>
      </div>
      <Divider />
      <h3>Task Summary</h3>
      <div class="flex align-item-center flex-wrap" style="min-height: 350px">
        <div class="chart-container">
          <template v-if="loadingComplete">
            <PieChart
              height="350"
              width="550"
              :task_list="task_info"
              :loadingComplete="loadingComplete"
              :workload="workload"
          /></template>
        </div>
        <div class="chart-container">
          <template v-if="loadingComplete">
            <BarChart
              height="350"
              width="550"
              :task_list="task_info"
              :loadingComplete="loadingComplete"
          /></template>
        </div>
      </div>
      <Divider />
      <h3>Tasks List</h3>
      <template v-if="loadingComplete">
        <Table
          :show_columns="task_columns"
          :task_list="task_info"
          :loadingComplete="loadingComplete"
        />
      </template>
      <Divider />
      <h3>Watch List</h3>
      <template v-if="loadingComplete2">
        <Table
          :show_columns="task_columns"
          :task_list="watch_list_info"
          :loadingComplete="loadingComplete2"
        />
      </template>
      <Divider />
      <h3>Connections</h3>
      <ConnectionList :connection_list="connection_list" :name="name" />
      <Divider />
    </div>
  </div>
</template>

<script>
import Avatar from 'primevue/avatar';
import Divider from 'primevue/divider';
import PieChart from '../components/PieChart';
import BarChart from '../components/BarChart';
import Table from '../components/Table';
import ConnectionList from '../components/ConnectionList';
import {
  getConectionList,
  getProfile,
  getTasks,
  getWatchList,
  getWorkload,
} from '../service/HttpService';

export default {
  name: 'Profile',
  mounted() {
    const token = localStorage.getItem('token');
    getProfile(token, this.$route.params.email).then((res) => {
      this.name = res.profile.user_name;
      this.email = res.profile.user_email;
    });
    this.loadingComplete = false;
    getTasks(token, this.$route.params.email)
      .then((res) => {
        this.task_list = res.task_list;
        this.loadingComplete = true;
      })
      .catch((err) => {
        console.log(err);
      });
    this.loadingComplete2 = false;
    getWatchList(token, this.$route.params.email)
      .then((res) => {
        this.watch_list = res.watching_list;
        this.loadingComplete2 = true;
      })
      .catch((err) => {
        console.log(err);
      });
    getConectionList(token, this.$route.params.email)
      .then((res) => {
        this.connection_list = res.connection_list;
      })
      .catch((err) => console.log(err));
    getWorkload(token, this.$route.params.email)
      .then((res) => {
        this.workload = res.workload;
      })
      .catch((err) => console.log(err));
  },
  data() {
    return {
      icon_image: '',
      name: {
        type: String,
        default: '',
      },
      email: '',
      workload: 0.0,
      loadingComplete: false,
      loadingComplete2: false,
      task_list: [],
      watch_list: [],
      task_columns: {
        name: true,
        assign_to: true,
        due_date: true,
        estimated_time: true,
        content: true,
        status: true,
        items_per_row: 5,
      },
      taskData: [],
      connection_list: [],
    };
  },
  components: {
    Avatar,
    Divider,
    PieChart,
    BarChart,
    Table,
    ConnectionList,
  },
  computed: {
    task_info() {
      return this.task_list;
    },
    watch_list_info() {
      return this.watch_list;
    },
  },
  methods: {},
};
</script>

<style scoped>
.name {
  font: 50px bolder;
}
.email {
  padding-left: 10px;
  font: 20px bold;
  font-family: Arial, Helvetica, sans-serif;
  color: #5d5c5c;
}
.chart-container {
  padding: 5px;
}
</style>
