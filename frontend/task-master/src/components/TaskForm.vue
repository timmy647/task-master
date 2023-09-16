<template>
  <div
    class="flex flex-row-reverse align-content-start justify-content-center"
    style="padding: 0 10%"
  >
    <div v-if="!create_new_task" class="flex" style="min-width: 180px">
      <div v-if="deletable">
        <span style="color: rgb(220, 0, 0); font-weight: Bold"
          >Do you want to delete this task?</span
        >
        <div class="flex flex-row">
          <i
            class="fa-solid fa-check clickable btn-size"
            @click="DeleteTask"
          ></i>
          &nbsp; &nbsp; &nbsp;
          <i
            class="fa-solid fa-x clickable btn-size"
            @click="toggleDeletable"
          ></i>
        </div>
      </div>
      <div v-else-if="!editable">
        <div class="flex flex-row">
          <i
            class="fa-solid fa-pen-to-square clickable btn-size"
            @click="toggleEditable"
          ></i>
          &nbsp; &nbsp; &nbsp;
          <i
            v-if="liked"
            class="fa-solid fa-heart clickable btn-size"
            @click="dislikeTask"
          ></i>
          <i
            v-else
            class="fa-regular fa-heart clickable btn-size"
            @click="likeTask"
          ></i>
          <!-- &nbsp; &nbsp; &nbsp;
          <i
            class="fa-solid fa-trash-can clickable btn-size"
            @click="toggleDeletable"
          ></i> -->
        </div>
      </div>
      <div v-else>
        <i
          class="fa-regular fa-floppy-disk clickable btn-size"
          @click="updateTask"
        ></i>
      </div>
    </div>

    <div style="min-width: 80%; min-height: 600px">
      <div class="field grid form-row">
        <label for="name" class="col-fixed" style="width: 100px">Name</label>
        <div class="col">
          <input
            v-if="editable"
            id="name"
            type="text"
            class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
            v-model="task.title"
          />
          <label v-if="!editable">{{ task.title ? task.title : '' }}</label>
        </div>
      </div>
      <div class="field grid">
        <label for="assignto" class="col-fixed" style="width: 100px"
          >Assign to</label
        >
        <div class="col">
          <!-- <input
            v-if="editable"
            id="assignto"
            type="text"
            class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
            v-model="task.assigned_user"
          /> -->
          <Dropdown
            editable
            id="assignto"
            v-if="editable"
            v-model="task.assigned_user"
            :options="connectedUsers"
            optionLabel="email"
            optionValue="email"
            optionGroupLabel="label"
            optionGroupChildren="items"
            placeholder="Select a Master"
            class="w-full md:w-14rem"
          >
            <template #optiongroup="slotProps">
              <div class="flex align-items-center">
                <div>{{ slotProps.option.label }}</div>
              </div>
            </template>
          </Dropdown>
          <label v-if="!editable">{{
            task.assigned_user !== undefined ? task.assigned_user : ''
          }}</label>
        </div>
      </div>
      <div class="field grid">
        <label for="date" class="col-fixed" style="width: 100px"
          >Deadline</label
        >
        <div class="col">
          <input
            v-if="editable"
            id="date"
            type="date"
            class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
            v-model="task.deadline"
          />
          <label v-if="!editable">{{
            task.deadline ? dateToString(task.deadline) : ''
          }}</label>
        </div>
      </div>
      <div class="field grid">
        <label for="estiamted_time" class="col-fixed" style="width: 100px"
          >Estimated Hours</label
        >
        <div class="col">
          <input
            v-if="editable"
            id="estiamted_time"
            type="number"
            class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
            v-model="task.task_estimated_time"
          />
          <label v-if="!editable">{{
            task.task_estimated_time ? task.task_estimated_time : ''
          }}</label>
        </div>
      </div>
      <div class="field grid">
        <label for="status" class="col-fixed" style="width: 100px"
          >Status</label
        >
        <div class="col">
          <Dropdown
            :disabled="create_new_task"
            v-if="editable"
            v-model="task.task_status"
            :options="status_options"
            placeholder="Select a Status"
            class="w-full md:w-14rem"
          />
          <Tag
            v-if="!editable"
            :value="task.task_status"
            :severity="getSeverity(task.task_status)"
          />
        </div>
      </div>
      <div class="field grid">
        <label for="content" class="col-fixed" style="width: 100px"
          >Description</label
        >
        <div class="col">
          <Textarea
            v-if="editable"
            id="content"
            type="text"
            rows="10"
            cols="45"
            class="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
            v-model="task.description"
          />
          <p v-if="!editable">{{ task.description ? task.description : '' }}</p>
        </div>
      </div>
      <div v-if="!editable" class="field grid">
        <label for="history" class="col-fixed" style="width: 100px"
          >History</label
        >
        <div class="col">
          <div v-if="!editable">
            <Timeline :value="events">
              <template #opposite="slotProps">
                <small class="p-text-secondary">{{
                  slotProps.item.updated_time
                }}</small>
              </template>
              <template #content="slotProps">
                {{ computeHistory(slotProps.item) }}
              </template>
            </Timeline>
          </div>
        </div>
      </div>
      <div v-if="create_new_task" class="flex flex-row-reverse">
        <Button @click="createTask">Create</Button>
      </div>
    </div>
  </div>
</template>

<script>
import { getHistory, getRecommended, updateTask } from '@/service/HttpService';
import { createTask } from '@/service/HttpService';
import Timeline from 'primevue/timeline';
import {
  checkWatched,
  getConectionList,
  watchCancel,
  watchTask,
} from '../service/HttpService';
export default {
  name: 'TaskForm',
  inject: ['dialogRef'],
  components: {
    Timeline,
  },
  created() {
    if (!this.create_new_task) {
      this.checkLiked();
      getHistory(this.token, this.task.task_id)
        .then((res) => {
          this.events = res.history;
        })
        .catch((err) => alert(err));
    }
    getConectionList(this.token, localStorage.getItem('email'))
      .then((res) => {
        this.connectedUsers[1].items = [
          {
            email: localStorage.getItem('email'),
          },
        ];
        this.connectedUsers[1].items = this.connectedUsers[1].items.concat(
          res.connection_list
        );
      })
      .catch((err) => alert(err));
    getRecommended(this.token)
      .then((res) => {
        this.connectedUsers[0].items = res.list;
      })
      .catch((err) => alert(err));
  },
  data() {
    return {
      liked: false,
      token: localStorage.getItem('token'),
      create_new_task: this.dialogRef.data.given_task ? false : true,
      deletable: false,
      task:
        this.dialogRef.data.given_task !== undefined
          ? this.dialogRef.data.given_task
          : {
              id: -1,
              title: '',
              deadline: new Date().toISOString().split('T')[0],
              assigned_user: '',
              task_status: 'Not Started',
              task_estimated_time: 0,
              description: '',
            },
      editable: this.dialogRef.data.given_task ? false : true,
      status_options: ['Not Started', 'In Progress', 'Completed', 'Blocked'],
      events: [],
      connectedUsers: [
        {
          label: 'Recommended',
          items: [],
        },
        {
          label: 'All Connected Master',
          items: [],
        },
      ],
    };
  },
  emits: ['info'],
  methods: {
    createTask() {
      createTask(this.token, this.task)
        .then(() => {
          this.dialogRef.close();
          this.$emit('info');
        })
        .catch((err) => {
          alert(err);
        });
    },
    toggleDeletable() {
      this.deletable = !this.deletable;
    },
    updateTask() {
      updateTask(this.token, this.task.task_id, this.task)
        .then(() => {
          this.toggleEditable();
        })
        .catch((err) => {
          alert(err);
        });
    },
    DeleteTask() {
      this.dialogRef.close();
    },
    toggleEditable() {
      this.editable = !this.editable;
    },
    likeTask() {
      watchTask(this.token, this.task.task_id)
        .then(() => {
          this.liked = true;
        })
        .catch((err) => alert(err));
    },
    dislikeTask() {
      watchCancel(this.token, this.task.task_id)
        .then(() => {
          this.liked = false;
        })
        .catch((err) => alert(err));
    },
    dateToString(date) {
      if (!date) {
        return '';
      } else if (typeof date !== Date) {
        date = new Date(date);
      }
      const year = parseInt(date.getFullYear());
      var month = parseInt(date.getMonth()) + 1;
      var day = parseInt(date.getDate());
      month = month < 10 ? '0' + month : month;
      day = day < 10 ? '0' + day : day;
      return year + '-' + month + '-' + day;
    },
    getSeverity(status) {
      switch (status) {
        case 'Blocked':
          return 'danger';

        case 'Completed':
          return 'success';

        case 'Not Started':
          return 'info';

        case 'In Progress':
          return 'warning';
      }
    },
    async checkLiked() {
      checkWatched(this.token, this.task.task_id)
        .then((res) => {
          this.liked = res.result;
        })
        .catch((err) => {
          alert(err);
        });
    },
    computeHistory(history) {
      let res = '';
      if (history.assigned_user !== undefined) {
        res += `Assign to ${history.assigned_user}; `;
      }
      if (history.task_status !== undefined) {
        res += `Updated status: ${history.task_status}; `;
      }
      if (history.title !== undefined) {
        res += `Updated title: ${history.title}; `;
      }
      if (history.deadline !== undefined) {
        res += `Updated deadline: ${
          new Date(history.deadline).toISOString().split('T')[0]
        }; `;
      }
      if (history.task_estimated_time !== undefined) {
        res += `Updated estimated hours: ${history.task_estimated_time}; `;
      }
      if (history.description !== undefined) {
        res += `Updated estimated hours: ${history.description}; `;
      }
      if (res == '') {
        res = 'No Update Changes';
      }
      return res;
    },
  },
  computed: {},
};
</script>

<style scoped>
div {
}
.btn-size {
  font-size: 30px;
}
</style>
