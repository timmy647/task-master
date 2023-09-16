<template>
  <div>
    <div class="sidebar">
      <div><router-link class="active" to="/home">Home</router-link></div>
      <div><router-link to="/tasks">My Tasks</router-link></div>
    </div>
    <div class="content">
      <h1>Welcome to Task Master!</h1>
      <h3>Tasks Summary</h3>
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
      <h3>Task Updates</h3>
      <div v-for="update in update_info" v-bind:key="update.id">
        <InfoCard
          type="task_update"
          :data="update"
          @click="openHistoryPopup(update.task_id)"
          class="clickable"
        />
      </div>
      <div v-if="tasks_updates === undefined || tasks_updates.length === 0">
        There are no connection invites.
      </div>
      <Divider />
      <h3>New Connections</h3>
      <div v-for="conection in new_connections" v-bind:key="conection.email">
        <InfoCard type="new_connection" :data="conection" />
      </div>
      <div v-if="new_connections.length === 0">
        There are no connection invites.
      </div>
      <Divider />
    </div>
  </div>
</template>

<script>
import Divider from 'primevue/divider';
import PieChart from '../components/PieChart';
import BarChart from '../components/BarChart';
import InfoCard from '../components/InfoCard';
import {
  getConectionRequests,
  getNotification,
  getTasks,
} from '@/service/HttpService';
import {
  getTaskDetail,
  getWorkload,
  watchHisotryUpdate,
} from '../service/HttpService';
import { defineAsyncComponent } from 'vue';
import { useDialog } from 'primevue/usedialog';
export default {
  name: 'Home',
  components: {
    PieChart,
    BarChart,
    Divider,
    InfoCard,
  },
  created() {
    const token = localStorage.getItem('token');
    this.loadingComplete = false;
    getTasks(token, localStorage.getItem('email'))
      .then((res) => {
        this.task_list = res.task_list;
        this.loadingComplete = true;
      })
      .catch((err) => {
        console.log(err);
      });
    getNotification(token)
      .then((res) => {
        this.tasks_updates = res.notification;
      })
      .catch((err) => {
        console.log(err);
      });
    getConectionRequests(token)
      .then((res) => {
        this.new_connections = res.connection_request_list;
      })
      .catch((err) => {
        console.log(err);
      });
    getWorkload(token, localStorage.getItem('email'))
      .then((res) => {
        this.workload = res.workload;
      })
      .catch((err) => console.log(err));
  },
  data() {
    return {
      workload: 0.0,
      loadingComplete: false,
      task_list: [],
      tasks_updates: [],
      new_connections: [],
      dialog: useDialog(),
      TaskForm: defineAsyncComponent(() =>
        import('../components/TaskForm.vue')
      ),
    };
  },
  methods: {
    openHistoryPopup(task_id) {
      getTaskDetail(localStorage.getItem('token'), task_id).then((res) => {
        const task = res.task;
        this.dialog.open(this.TaskForm, {
          props: {
            header: 'Task ID: ' + task.task_id,
            style: {
              width: '50vw',
            },
            breakpoints: {
              '960px': '75vw',
              '640px': '90vw',
            },
            modal: true,
          },
          data: {
            given_task: task,
          },
          templates: {},
          onClose: () => {
            const token = localStorage.getItem('token');
            watchHisotryUpdate(token, task_id)
              .then((res) => {
                console.log(res);
                getNotification(token)
                  .then((res) => {
                    console.log(res);
                    this.tasks_updates = res.notification;
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              })
              .catch((err) => alert(err));
          },
        });
      });
    },
  },
  computed: {
    task_info() {
      return this.task_list;
    },
    update_info() {
      return this.tasks_updates;
    },
  },
};
</script>

<style scoped>
.chart-container {
  padding: 5px;
}
</style>
