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
        <TaskMenu /><Button style="margin: 10px" @click="showNewTaskForm"
          ><i class="fa-regular fa-file"></i>&nbsp; New Task</Button
        >
      </div>
      <template v-if="loadingComplete">
        <Table
          :show_columns="task_columns"
          :task_list="task_info"
          :loadingComplete="loadingComplete"
        />
      </template>
    </div>
  </div>
</template>

<script>
import TaskMenu from '../components/TaskMenu';
import Table from '../components/Table';
import { defineAsyncComponent } from 'vue';
import { useDialog } from 'primevue/usedialog';

import { getTasks } from '../service/HttpService';

export default {
  name: 'TaskTableView',
  components: {
    TaskMenu,
    Table,
  },
  created() {
    this.loadingComplete = false;
    const token = localStorage.getItem('token');
    getTasks(token, localStorage.getItem('email'))
      .then((res) => {
        this.task_columns.task_list = res.task_list;
        this.task_list = res.task_list;
        this.loadingComplete = true;
      })
      .catch((err) => {
        console.log(err);
      });
  },
  data() {
    return {
      loadingComplete: false,
      task_list: [],
      task_columns: {
        name: true,
        assign_to: true,
        due_date: true,
        estimated_time: true,
        content: true,
        status: true,
        items_per_row: 8,
        task_list: [],
      },
      dialog: useDialog(),
      TaskForm: defineAsyncComponent(() =>
        import('../components/TaskForm.vue')
      ),
    };
  },
  computed: {
    task_info() {
      return this.task_list;
    },
  },
  methods: {
    showNewTaskForm() {
      this.dialog.open(this.TaskForm, {
        props: {
          header: 'Create a New Task',
          style: {
            width: '50vw',
          },
          breakpoints: {
            '960px': '75vw',
            '640px': '90vw',
          },
          modal: true,
        },
        data() {},
        emits: {
          onInfo: () => {
            console.log('emitting');
            this.get_tasks();
          },
        },
        templates: {},
        onClose: () => {},
      });
    },
    get_tasks() {
      this.loadingComplete = false;
      const token = localStorage.getItem('token');
      getTasks(token, localStorage.getItem('email'))
        .then((res) => {
          this.task_columns.task_list = res.task_list;
          this.task_list = res.task_list;
          this.loadingComplete = true;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
