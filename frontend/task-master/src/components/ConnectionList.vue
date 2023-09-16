<template>
  <div class="card">
    <DataTable
      v-model:filters="filters"
      :value="connection_list"
      paginator
      :rows="5"
      tableStyle="min-width: 50rem"
    >
      <template #header>
        <div class="flex justify-content-between flex-wrap">
          <span class="p-input-icon-left title">{{ name }}'s Connections</span>
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              placeholder="Keyword Search"
            />
          </span>
        </div>
      </template>
      <Column sortable field="name" header="Name" style="width: 25%">
        <template #body="{ data }">
          <span class="clickable" @click="navigate2Profile(data.email)">{{
            data.name
          }}</span>
        </template>
      </Column>
      <Column sortable field="email" header="Email" style="width: 75%">
        <template #body="{ data }">
          <span class="clickable" @click="navigate2Profile(data.email)">{{
            data.email
          }}</span>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { FilterMatchMode, FilterOperator } from 'primevue/api';

export default {
  name: 'ConnectionList',
  components: {
    DataTable,
    Column,
  },
  props: {
    connection_list: {
      type: Array,
      default() {
        return [];
      },
    },
    name: {
      type: String,
      default() {
        return '';
      },
    },
  },
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        name: {
          operator: FilterOperator.AND,
          constraints: [
            { value: null, matchMode: FilterMatchMode.STARTS_WITH },
          ],
        },
      },
    };
  },
  methods: {
    navigate2Profile(email) {
      this.$router.push(`/user/${email}`).then(() => {
        window.scrollTo(0, 0);
      });
    },
  },
};
</script>

<style scoped>
.card {
  padding: 0 5px;
}

.title {
  font-size: 30px;
  font: bolder;
}
</style>
