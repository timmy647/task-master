Taskview.vue
<template>
  <TabMenu :model="items" />
</template>

<script>
import TabMenu from 'primevue/tabmenu';
export default {
  name: 'TasksView',
  components: {
    TabMenu,
  },
  data() {
    return {
      items: [
        {
          label: 'Home',
          icon: 'pi pi-fw pi-home',
          to: '/',
        },
        {
          label: 'Calendar',
          icon: 'pi pi-fw pi-calendar',
          to: '/calendar',
        },
        {
          label: 'Edit',
          icon: 'pi pi-fw pi-pencil',
          to: '/edit',
        },
        {
          label: 'Documentation',
          icon: 'pi pi-fw pi-file',
          to: '/documentation',
        },
        {
          label: 'Settings',
          icon: 'pi pi-fw pi-cog',
          to: '/settings',
        },
      ],
    };
  },
};
</script>
