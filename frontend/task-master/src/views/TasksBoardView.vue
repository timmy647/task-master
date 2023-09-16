<template>
  <div>
    <div class="sidebar">
      <div><router-link to="/home">Home</router-link></div>
      <div>
        <router-link class="active" to="/tasks">My Tasks</router-link>
      </div>
    </div>
    <div class="content">
      <div class="flex flex-row justify-content-between">
        <TaskMenu /><Button style="margin: 10px" @click="showNewTaskForm"
          ><i class="fa-regular fa-file"></i>&nbsp; New Task</Button
        >
      </div>
      <div class="kanban-board">
        <div
          class="kanban-column"
          v-for="status in statuses"
          :key="status"
          :data-status="status"
        >
          <h2 :class="statusHeaderColor(status)">{{ status }}</h2>
          <draggable
            class="kanban-card"
            :list="paginatedTasks[status] || []"
            group="tasks"
            @change="updateTaskStatus(status, $event)"
            :move="checkMove"
            itemKey="task_id"
            style="line-height: 5px"
          >
            <template #item="{ element }">
              <div
                :key="element.task_id"
                class="task-container clickable"
                :class="statusBoxColor(element.task_status)"
                @click="showTaskForm(element)"
              >
                <h2 style="line-height: 30px">{{ element.title }}</h2>
                <p style="line-height: 20px">
                  Due on {{ formatDate(element.deadline) }}
                </p>
              </div>
            </template>
          </draggable>
          <div
            v-if="!taskMap[status] || taskMap[status].length === 0"
            class="no-tasks"
          >
            No Tasks
          </div>
          <div class="flex align-items-center justify-content-center">
            <Button
              :disabled="currentPage[status] <= 0"
              @click="currentPage[status]--"
            >
              <i class="fa-solid fa-arrow-left"></i>
            </Button>
            <span
              >&nbsp;
              {{ currentPage[status] + 1 }}
              &nbsp;
            </span>
            <Button
              :disabled="
                taskMap[status] &&
                taskMap[status].length <=
                  (currentPage[status] + 1) * tasksPerPage
              "
              @click="currentPage[status]++"
            >
              <i class="fa-solid fa-arrow-right"></i>
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import TaskMenu from '../components/TaskMenu';
import { getTasks, updateTask } from '../service/HttpService';
import { defineAsyncComponent } from 'vue';
import { useDialog } from 'primevue/usedialog';
export default {
  name: 'TaskBoardView',
  components: {
    TaskMenu,
    draggable,
  },
  data() {
    return {
      tasks: [],
      statuses: ['Not Started', 'In Progress', 'Blocked', 'Completed'], // Update this list as necessary
      tasksPerPage: 5,
      currentPage: {
        'Not Started': 0,
        'In Progress': 0,
        Blocked: 0,
        Completed: 0,
      },
      dialog: useDialog(),
      TaskForm: defineAsyncComponent(() =>
        import('../components/TaskForm.vue')
      ),
    };
  },
  async mounted() {
    this.tasks = await getTasks(
      localStorage.getItem('token'),
      localStorage.getItem('email')
    );
    this.tasks = this.tasks.task_list;
  },
  computed: {
    taskMap() {
      return this.tasks.reduce((map, task) => {
        if (!map[task.task_status]) map[task.task_status] = [];
        map[task.task_status].push(task);
        return map;
      }, {});
    },
    paginatedTasks() {
      let paginated = {};
      for (let status of this.statuses) {
        if (!this.taskMap[status]) continue;
        paginated[status] = this.taskMap[status].slice(
          this.currentPage[status] * this.tasksPerPage,
          (this.currentPage[status] + 1) * this.tasksPerPage
        );
      }
      return paginated;
    },
  },
  methods: {
    statusHeaderColor(status) {
      switch (status.toLowerCase()) {
        case 'completed':
          return 'green-header';
        case 'blocked':
          return 'red-header';
        case 'in progress':
          return 'orange-header';
        case 'not started':
          return 'blue-header';
        default:
          return '';
      }
    },
    statusBoxColor(status) {
      switch (status.toLowerCase()) {
        case 'completed':
          return 'green-box';
        case 'blocked':
          return 'red-box';
        case 'in progress':
          return 'orange-box';
        case 'not started':
          return 'blue-box';
        default:
          return '';
      }
    },
    formatDate(value) {
      return new Date(value).toISOString().split('T')[0];
    },
    checkMove() {
      return true;
    },

    log(event) {
      console.log(event);
    },
    updateTaskStatus(status, event) {
      if (event.added) {
        let updated_task = event.added.element;
        updated_task.task_status = status;
        updateTask(
          localStorage.getItem('token'),
          updated_task.task_id,
          updated_task
        )
          .then(() => {})
          .catch((err) => alert(err));
      }
    },
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
            this.get_tasks();
          },
        },
        templates: {},
        onClose: () => {},
      });
    },
    showTaskForm(task) {
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
        onClose: () => {},
      });
    },
    get_tasks() {
      this.loadingComplete = false;
      const token = localStorage.getItem('token');
      getTasks(token, localStorage.getItem('email'))
        .then((res) => {
          this.tasks = res.task_list;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
.kanban-board {
  display: flex;
  justify-content: space-around;
}
.kanban-column {
  width: 100%;
  padding: 1em;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #f4f4f4;
}
.kanban-card {
  padding: 1em;
  margin: 0;
  border: 2px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.blue-header {
  color: blue;
}
.orange-header {
  color: orange;
}
.light-green-header {
  color: lightgreen;
}
.green-header {
  color: lightgreen;
}

.red-header {
  color: red;
}

.orange-header {
  color: orange;
}

.blue-header {
  color: blue;
}
.blue-box {
  background-color: lightblue;
}
.orange-box {
  background-color: orange;
}
.light-green-box {
  background-color: #e8f5e9;
}
.green-box {
  background-color: lightgreen;
}

.red-box {
  background-color: #ff7f7f;
}

.orange-box {
  background-color: orange;
}

.blue-box {
  background-color: lightblue;
}
.task-container {
  padding: 1em;
  margin: 1em 0;
  border: 2px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.no-tasks {
  font-size: 1.5em; /* Adjusted from 1.2em to 1.5em */
  color: #888;
  text-align: center;
  padding: 1em;
}

@media screen and (max-width: 600px) {
  .kanban-board {
    flex-direction: column;
  }
  .kanban-column {
    width: 100%;
  }
}
</style>
