<template>
  <div class="card">
    <DataTable
      v-model:filters="filters"
      :value="tasks"
      paginator
      removableSort
      showGridlines
      :rows="show_columns.items_per_row"
      dataKey="id"
      filterDisplay="menu"
      :loading="loading"
      :globalFilterFields="[
        'title',
        'assign_user',
        'deadline',
        'description',
        'task_status',
      ]"
    >
      <template #header>
        <div class="flex justify-content-between">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            label="Clear"
            outlined
            @click="clearFilter()"
          />
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              placeholder="Keyword Search"
            />
          </span>
        </div>
      </template>
      <template #empty> No tasks found. </template>
      <template #loading> Loading tasks data. Please wait. </template>
      <Column
        sortable
        field="title"
        header="Name"
        style="min-width: 12rem"
        v-if="show_columns.name"
      >
        <template #body="{ data }">
          <span @click="showTaskForm(data)" class="clickable">{{
            data.title
          }}</span>
        </template>
        <template #filter="{ filterModel }">
          <InputText
            v-model="filterModel.value"
            type="text"
            class="p-column-filter"
            placeholder="Search by name"
          />
        </template>
      </Column>
      <Column
        v-if="show_columns.assign_to"
        header="Assign To"
        filterField="assigned_user"
        :showFilterMatchModes="false"
        :filterMenuStyle="{ width: '14rem' }"
        style="min-width: 14rem"
      >
        <template #body="{ data }">
          <div class="flex align-items-center gap-2">
            <Avatar
              icon="pi pi-user"
              class="mr-2"
              size="large"
              shape="circle"
            />
            <span
              class="clickable"
              @click="navigate2Profile(data.assigned_user)"
              >{{ data.assigned_user }}</span
            >
          </div>
        </template>
        <template #filter="{ filterModel }">
          <InputText
            v-model="filterModel.value"
            type="text"
            class="p-column-filter"
            placeholder="Search by name"
          />
        </template>
      </Column>
      <Column
        v-if="show_columns.due_date"
        header="Date"
        filterField="deadline"
        dataType="date"
        style="min-width: 10rem"
      >
        <template #body="{ data }">
          {{ formatDate(data.deadline) }}
        </template>
        <template #filter="{ filterModel }">
          <Calendar
            v-model="filterModel.value"
            dateFormat="mm/dd/yy"
            placeholder="mm/dd/yyyy"
            mask="99/99/9999"
          />
        </template>
      </Column>
      <Column
        sortable
        v-if="show_columns.estimated_time"
        header="Estimated Hours"
        field="task_estimated_time"
        dataType="numeric"
        style="min-width: 10rem"
        :showFilterMatchModes="false"
      >
        <template #body="{ data }">
          {{ formatHour(data.task_estimated_time) }}
        </template>
        <template #filter="{ filterModel }">
          <Slider v-model="filterModel.value" range class="m-3"></Slider>
          <div class="flex align-items-center justify-content-between px-2">
            <span>{{ filterModel.value ? filterModel.value[0] : 0 }}</span>
            <span>{{ filterModel.value ? filterModel.value[1] : 1 }}</span>
          </div>
        </template>
      </Column>
      <Column
        sortable
        v-if="show_columns.status"
        header="Status"
        field="task_status"
        :filterMenuStyle="{ width: '14rem' }"
        style="min-width: 12rem"
      >
        <template #body="{ data }">
          <Tag
            :value="data.task_status"
            :severity="getSeverity(data.task_status)"
          />
        </template>
        <template #filter="{ filterModel }">
          <Dropdown
            v-model="filterModel.value"
            :options="statuses"
            placeholder="Select One"
            class="p-column-filter"
            showClear
          >
            <template #option="slotProps">
              <Tag
                :value="slotProps.option"
                :severity="getSeverity(slotProps.option)"
              />
            </template>
          </Dropdown>
        </template>
      </Column>
      <Column
        v-if="show_columns.content"
        header="Content"
        filterField="description"
        dataType="numeric"
        style="min-width: 10rem"
      >
        <template #body="{ data }">
          {{ data.description }}
        </template>
        <template #filter="{ filterModel }">
          <InputText
            v-model="filterModel.value"
            type="text"
            class="p-column-filter"
            placeholder="Search by keywords"
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, toRefs } from 'vue';
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import { useDialog } from 'primevue/usedialog';

const props = defineProps(['show_columns', 'task_list', 'loadingComplete']);
const { show_columns, task_list, loadingComplete } = toRefs(props);
const filters = ref();
const tasks = ref();
const statuses = ref(['Blocked', 'Not Started', 'In Progress', 'Completed']);
const loading = ref(true);
var maxHour = ref(100);

onMounted(() => {
  tasks.value = StringtoDate(task_list.value);
  loading.value = !loadingComplete.value;
  maxHour.value = 100;
});

const StringtoDate = (data) => {
  return [...(data || [])].map((d) => {
    if (d.deadline) {
      d.deadline = new Date(d.deadline);
    }
    return d;
  });
};

const initFilters = () => {
  filters.value = {
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    title: {
      operator: FilterOperator.AND,
      constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
    },
    assigned_user: { value: null, matchMode: FilterMatchMode.IN },
    deadline: {
      operator: FilterOperator.AND,
      constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
    },
    task_estimated_time: {
      value: [0, 100],
      matchMode: FilterMatchMode.BETWEEN,
    },
    description: {
      operator: FilterOperator.AND,
      constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
    },
    task_status: {
      operator: FilterOperator.OR,
      constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
    },
  };
};

initFilters();

const formatDate = (value) => {
  if (typeof value !== Date) {
    value = new Date(value);
  }
  return value.toLocaleDateString('en-US', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
};

const formatHour = (value) => {
  return value;
};

const clearFilter = () => {
  initFilters();
};

// const StringtoDate = (data) => {
//   console.log(data);
//   return [...(data || [])].map((d) => {
//     if (d.date) {
//       d.date = new Date(d.date);
//     }
//     return d;
//   });
// };

const getSeverity = (status) => {
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
};

import { defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';
const dialog = useDialog();
const TaskForm = defineAsyncComponent(() => import('./TaskForm.vue'));

const showTaskForm = (task) => {
  dialog.open(TaskForm, {
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
};

const router = useRouter();
function navigate2Profile(email) {
  router.push({ path: `/user/${email}` }).then(() => {
    window.scrollTo(0, 0);
  });
}
</script>

<style scoped>
.card {
  padding: 0 5px;
}
</style>
