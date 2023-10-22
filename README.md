# Task Master

![Task Master](/task-master.png?raw=true "Screenshot")

## Overview

**Task Master** is a collaborative task management web application designed to help teams effectively manage tasks and workloads. Whether you're working on a project, running a business, or simply trying to stay organized, Task Master provides the tools and features to keep your team on track.

## Features

- **Task Management**: Create, assign, and prioritize tasks. Keep an overview of tasks that need attention and completion.

- **Team Collaboration**: Collaborate with your team members by sharing tasks, comments, and updates in real-time.

- **Workload Management**: Visualize workloads and distribute tasks evenly to optimize productivity.

- **Progress Tracking**: Monitor task progress with visual charts and graphs powered by ChartJS.

## Technologies Used

- **Vue 3**: The frontend is built with Vue 3, a progressive JavaScript framewors.

- **PrimeVue and ChartJS**: PrimeVue for a rich set of UI components, and ChartJS for a various set of Chart components are used.

- **Flask**: The backend server is powered by Flask, a lightweight Python web framework, to handle task management and user interactions.

- **PostgreSQL**: PostgreSQL is used as the database to store task and user data securely.


## Getting Start

```
git clone https://github.com/unsw-cse-comp3900-9900-23T2/capstone-project-3900h18anofail.git
cd task-master
```

### How to run frontend

```
cd frontend/
npm install
npm run serve
```

### How to run Backend
```
cd backend/
python server.py
```

### How to deploy database
run backend/schema.sql in PostgreSQL 13
