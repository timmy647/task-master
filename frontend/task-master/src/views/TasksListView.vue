<template>
  <div>
    <div class="sidebar">
      <div><router-link to="/home">Home</router-link></div>
      <div>
        <router-link class="active" to="/tasks">My Tasks</router-link>
      </div>
    </div>
    <div class="content">
      <TaskMenu />
      <div class="task-list">
        <div class="task-item" :class="statusBoxColor(task.status)" v-for="(task, index) in tasks" :key="index">
          <h3>{{ task.name }}</h3>
          <p>Status: {{ task.status }}</p>
          <p>Due: {{ formatDate(task.due_date) }}</p>
          <p>Assigned to: {{ task.assign_to }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TaskMenu from '../components/TaskMenu';
import { ListService } from '../service/ListService';

export default {
  name: 'TaskListView',
  components: {
    TaskMenu,
  },
  data() {
    return {
      tasks: [],
    };
  },
  async mounted() {
    this.tasks = await ListService.getData();
  },
  methods: {
    statusBoxColor(status) {
      if (status === 'Not Started') {
        return 'blue-box';
      } else if (status === 'In Progress') {
        return 'orange-box';
      } else if (status === 'Completed') {
        return 'light-green-box';
      } else if (status === 'Blocked') {
        return 'red-box';
      }
    },
    formatDate(value) {
      if (!value) return '';
      return new Intl.DateTimeFormat().format(value);
    },
  },
};
</script>

<style scoped>
.task-list {
  display: flex;
  flex-direction: column;
  margin: 1em 0;
}
.task-item {
  padding: 1em;
  margin-bottom: 1em;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}
.blue-box {
  background-color: #e0f7fa;
}
.orange-box {
  background-color: #fff3e0;
}
.light-green-box {
  background-color: #e8f5e9;
}
.red-box {
  background-color: #ffebee;
}
</style>