export const TaskService = {
  getData() {
    return [
      {
        id: 1,
        name: 'IPhone 15',
        due_date: new Date(Date.UTC(2012, 1, 20, 3, 0, 0)),
        assign_to: 'Tim Cook',
        status: 'Completed',
        estimated_time: 1,
        content: 'Lauch iPhone 15',
      },
      {
        id: 2,
        name: 'Vision Pro 2',
        due_date: new Date(Date.UTC(2012, 11, 2, 3, 0, 0)),
        assign_to: 'Tim Cook',
        status: 'Not Started',
        estimated_time: 2,
        content: 'Lauch Vision Pro 2',
      },
      {
        id: 3,
        name: 'IPhone 14',
        due_date: new Date(Date.UTC(2012, 12, 20, 3, 2, 0)),
        assign_to: 'Tim Cook',
        status: 'Completed',
        estimated_time: 4,
        content: 'Lauch iPhone 14',
      },
      {
        id: 4,
        name: 'IPad Pro 2',
        due_date: new Date(Date.UTC(2012, 2, 20, 3, 0, 0)),
        assign_to: 'Tim Cook',
        status: 'Blocked',
        estimated_time: 2,
        content: 'Lauch Vision Pro 2',
      },
      {
        id: 5,
        name: 'IPhone 15 Pro',
        due_date: new Date(Date.UTC(2012, 11, 23, 3, 0, 1)),
        assign_to: 'Tim Cook',
        status: 'In Progress',
        estimated_time: 6,
        content: 'Lauch iPhone 15 Pro',
      },
      {
        id: 6,
        name: 'Mac Pro 2',
        due_date: new Date(Date.UTC(2012, 7, 20, 3, 0, 8)),
        assign_to: 'Tim Cook',
        status: 'Not Started',
        estimated_time: 3,
        content: 'Lauch Mac Pro 2',
      },
      {
        id: 7,
        name: 'IPhone 16',
        due_date: new Date(Date.UTC(2011, 11, 20, 3, 0, 0)),
        assign_to: 'Tim Cook',
        status: 'In Progress',
        estimated_time: 2,
        content: 'Lauch iPhone 16',
      },
      {
        id: 8,
        name: 'Apple Watch 2',
        due_date: new Date(Date.UTC(2004, 11, 20, 3, 0, 0)),
        assign_to: 'Tim Cook',
        status: 'Completed',
        estimated_time: 1,
        content: 'Lauch Apple Watch 2',
      },
    ];
  },

  getTasksSmall() {
    return Promise.resolve(this.getData().slice(0, 10));
  },

  getTasksMedium() {
    return Promise.resolve(this.getData().slice(0, 50));
  },

  getTasksLarge() {
    return Promise.resolve(this.getData().slice(0, 200));
  },

  getTasksXLarge() {
    return Promise.resolve(this.getData());
  },

  updateTaskStatus(id, newStatus) {
    const task = this.getData().find(task => task.id === id);
    if (task) {
      task.status = newStatus;
    }
  }
};
