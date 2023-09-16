<template>
  <div>
    <div class="sidebar">
      <div><router-link to="/home">Home</router-link></div>
      <div>
        <router-link class="active" to="/tasks/table">My Tasks</router-link>
      </div>
    </div>
    <div class="content">
      <div class="flex flex-row justify-content-between">
        <TaskMenu /><Button style="margin: 10px"
          ><i class="fa-regular fa-file"></i>&nbsp; New Task</Button
        >
      </div>
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
    </div>
  </div>
</template>
<script>
import TaskMenu from '../components/TaskMenu';
import PieChart from '../components/PieChart';
import BarChart from '../components/BarChart';
import { getTasks, getWorkload } from '../service/HttpService';

export default {
  name: 'TasksChartView',
  components: {
    TaskMenu,
    PieChart,
    BarChart,
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
        alert(err);
      });
    getWorkload(token, localStorage.getItem('email'))
      .then((res) => {
        this.workload = res.workload;
      })
      .catch((err) => console.log(err));
  },
  data() {
    return {
      loadingComplete: false,
      workload: 0.0,
      task_list: [],
    };
  },
  computed: {
    task_info() {
      return this.task_list;
    },
  },
};
</script>

<style>
.chart-container {
  padding: 5px;
}
</style>
