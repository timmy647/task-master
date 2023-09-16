<template>
  <div style="margin-top: 5px">
    <div v-if="type === 'task_update'">
      <Card>
        <template #content>
          <div class="flex flex-row">
            <Avatar
              icon="pi pi-book"
              class="mr-2"
              size="large"
              shape="circle"
            />
            <div class="flex flex-column">
              <span class="title"> {{ data.title }} </span>
              <span>There is a update on {{ data.title }}</span>
            </div>
          </div>
        </template>
      </Card>
    </div>
    <div v-else-if="type === 'new_connection'">
      <Card>
        <template #content>
          <div class="flex flex-row">
            <Avatar
              icon="pi pi-user"
              class="mr-2"
              size="large"
              shape="circle"
            />
            <div class="flex flex-column">
              <span
                class="title clickable"
                @click="this.$router.push(`/user/${data.email}`)"
              >
                {{ data.email }}
              </span>
              <span class="flex flex-wrap"
                >{{ data.name }} wants to connect with you. &nbsp;&nbsp;
                <div v-if="response === ''">
                  <i
                    class="fa-solid fa-check clickable icon-size"
                    v-on:click="acceptConnectionRequest(data.email)"
                  ></i>
                  &nbsp;&nbsp;
                  <i
                    class="fa-solid fa-x clickable icon-size"
                    v-on:click="rejectConnectionRequest(data.email)"
                  ></i>
                </div>
                <div v-else>({{ response }})</div>
              </span>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script>
import { connectionReceive } from '@/service/HttpService';

export default {
  name: 'InfoCard',
  created() {},
  data() {
    return {
      response: '',
    };
  },
  props: {
    type: {
      type: String,
      default: '',
    },
    data: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  methods: {
    acceptConnectionRequest(email) {
      connectionReceive(localStorage.getItem('token'), email, 'Accepted')
        .then((res) => {
          console.log(res);
          this.response = 'accepted';
          alert(res.message);
        })
        .catch((err) => {
          console.log(err);
          alert(err);
        });
    },
    rejectConnectionRequest(email) {
      connectionReceive(localStorage.getItem('token'), email, 'Rejected')
        .then((res) => {
          console.log(res);
          this.response = 'rejected';
          alert(res.message);
        })
        .catch((err) => {
          console.log(err);
          alert(err);
        });
    },
  },
};
</script>

<style scoped>
.title {
  font-weight: bolder;
}
</style>
