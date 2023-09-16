Taskmenu.vue
<template>
  <TabMenu :model="items" />
</template>

<script>
import TabMenu from 'primevue/tabmenu';
export default {
  name: 'TaskMenu',
  components: {
    TabMenu,
  },
  data() {
    return {
      items: [
        {
          label: 'Board',
          icon: 'pi pi-fw pi-calendar',
          to: '/tasks/board',
        },
        {
          label: 'Table',
          icon: 'pi pi-fw pi-table',
          to: '/tasks/table',
        },
        {
          label: 'Chart',
          icon: 'pi pi-fw pi-chart-bar',
          to: '/tasks/chart',
        },
      ],
    };
  },
};
</script>
