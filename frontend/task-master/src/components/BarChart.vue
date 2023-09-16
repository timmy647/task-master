<template>
  <div class="flex flex-row flex-wrap column-gap-4 container" :style="cssVars">
    <Bar :data="computedData" :options="options" />
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';
import { Bar } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'BarChart',
  components: {
    Bar,
  },
  props: {
    task_list: {
      type: Array,
      default() {
        return [];
      },
    },
    loadingComplete: {
      type: Boolean,
      default: true,
    },
    height: {
      type: String,
      default: '300',
    },
    width: {
      type: String,
      default: '600',
    },
  },
  computed: {
    cssVars() {
      return {
        height: this.height + 'px',
        width: this.width + 'px',
      };
    },
    computedData() {
      this.calculatedNumbers();
      return this.data;
    },
  },
  data() {
    return {
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
          {
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)',
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)',
            ],
            borderWidth: 1,
            data: [0, 0, 0, 0, 0, 0, 0],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Upcoming Tasks in the Next 7 Days',
          },
          legend: {
            display: false,
          },
        },
      },
    };
  },
  methods: {
    calculatedNumbers() {
      const today = new Date();
      const numsOfDays = 7;
      var days = Array(numsOfDays).fill(new Date());
      for (const i in days) {
        days[i] = new Date(today.getTime() + i * 24 * 60 * 60 * 1000);
        this.data.labels[i] = days[i].toISOString().split('T')[0];
      }
      for (const task of this.task_list) {
        for (let i = 0; i <= 6; i++) {
          if (
            new Date(task.deadline).toISOString().split('T')[0] ===
            days[i].toISOString().split('T')[0]
          ) {
            this.data.datasets[0].data[i] += 1;
          }
        }
      }
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
</style>
