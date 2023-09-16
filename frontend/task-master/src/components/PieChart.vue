<template>
  <div class="flex flex-row flex-wrap column-gap-4 container" :style="cssVars">
    <div class="flex flex-column flex-wrap justify-content-evenly">
      <div
        v-for="(num, index) in computedNumbers"
        v-bind:key="index"
        style="padding: 10px"
      >
        <div class="box-container" :style="workloadColor(index, num)">
          <div class="flex-1 word" :style="workloadColor(index, num)">
            {{ labels[index] }}
          </div>
          <div class="flex-1 number" :style="workloadColor(index, num)">
            {{ num }}
          </div>
        </div>
      </div>
    </div>
    <div v-if="loadingComplete">
      <Pie :data="chartData" :options="chartOptions" style="padding: 5px" />
    </div>
  </div>
</template>
<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'vue-chartjs';

ChartJS.register(ArcElement, Tooltip, Legend);
export default {
  name: 'PieChart',
  components: { Pie },
  created() {},
  computed: {
    cssVars() {
      return {
        height: this.height + 'px',
        width: this.width + 'px',
      };
    },
    computedChartData() {
      this.calculatedNumbers();
      return this.chartData;
    },
    computedNumbers() {
      this.calculatedNumbers();
      return this.numbers;
    },
  },
  props: {
    task_list: {
      type: Array,
      default() {
        return [];
      },
    },
    workload: {
      type: Number,
      default: 0.1,
    },
    loadingComplete: {
      type: Boolean,
      default: true,
    },
    height: {
      type: String,
      default: '310',
    },
    width: {
      type: String,
      default: '550',
    },
    chartOptions: {
      type: Object,
      default() {
        return {
          responsive: true,
          maintainAspectRatio: false,
        };
      },
    },
  },
  data() {
    return {
      numbers: [0, 0, 0],
      labels: ['Workload Next Week', 'Not Started', 'In Progress'],
      chartData: {
        labels: ['Not Started', 'In Progress', 'Completed', 'Blocked'],
        datasets: [
          {
            backgroundColor: ['#3B82F6', '#F59E0B', '#22C55E', '#EF4444'],
            data: [0, 0, 0, 0],
          },
        ],
      },
    };
  },
  methods: {
    calculatedNumbers() {
      var notStarted = 0;
      var inProgress = 0;
      var completed = 0;
      var blocked = 0;
      for (const task of this.task_list) {
        if (task.task_status === 'Not Started') {
          notStarted += 1;
        } else if (task.task_status === 'In Progress') {
          inProgress += 1;
        } else if (task.task_status === 'Completed') {
          completed += 1;
        } else {
          blocked += 1;
        }
      }
      this.numbers[0] = this.workload * 100 + '%';
      this.numbers[1] = notStarted;
      this.numbers[2] = inProgress;
      this.chartData.datasets[0].data[0] = notStarted;
      this.chartData.datasets[0].data[1] = inProgress;
      this.chartData.datasets[0].data[2] = completed;
      this.chartData.datasets[0].data[3] = blocked;
    },
    workloadColor(index, percentage) {
      percentage = parseFloat(percentage);
      let res_color = 'green';
      if (index === 0) {
        if (percentage < 50) {
          res_color = 'green';
        } else if (percentage < 75) {
          res_color = 'orange';
        } else {
          res_color = 'red';
        }
      } else {
        if (percentage < 10) {
          res_color = 'green';
        } else if (percentage < 20) {
          res_color = 'orange';
        } else {
          res_color = 'red';
        }
      }
      return { color: res_color, 'border-color': res_color };
    },
  },
};
</script>

<style scoped>
@import '../styles/constant.css';
.container {
  border-style: solid;
  border-radius: 15px;
  border-color: var(--hoverColor);
}
.box-container {
  height: 80px;
  width: 140px;
  border-style: solid;
  border-radius: 15px;
  border-color: var(--activeColor);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding-left: 10px;
}
.word {
  height: 60px;
  color: var(--activeColor);
}

.number {
  font-size: 30px;
  color: var(--fontColor);
}
</style>
