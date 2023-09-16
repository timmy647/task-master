const URL = 'http://127.0.0.1:5000';

async function catchError(response) {
  if (response.status >= 400 && response.status < 600) {
    const err = await response.json();
    return await Promise.reject(new Error(err.message));
  }
  return await response.json();
}

export async function authLogin(email, password) {
  const data = {
    email,
    password,
  };
  var response = await fetch(URL + '/auth/login', {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return catchError(response);
}

export async function authRegister(email, password, name) {
  const data = {
    email,
    password,
    name,
  };
  var response = await fetch(URL + '/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function authLogout(token) {
  var response = await fetch(URL + '/auth/logout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function getProfile(token, email) {
  var response = await fetch(URL + `/profile?email=${email}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function profileSearch(token, email) {
  const data = {
    email,
  };
  var response = await fetch(URL + '/profile/search', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function getTasks(token, email) {
  var response = await fetch(URL + `/task/list?email=${email}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function getTaskDetail(token, task_id) {
  var response = await fetch(URL + `/task/detail?task_id=${task_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function createTask(token, task) {
  const data = {
    task: {
      title: task.title,
      assigned_user: task.assigned_user,
      description: task.description,
      deadline: new Date(task.deadline).toISOString().split('T')[0],
      task_estimated_time: task.task_estimated_time,
      task_status: task.task_status,
    },
  };
  var response = await fetch(URL + '/task/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function updateTask(token, task_id, task) {
  const data = {
    task_id,
    task: {
      title: task.title,
      assigned_user: task.assigned_user,
      description: task.description,
      deadline: new Date(task.deadline).toISOString().split('T')[0],
      task_estimated_time: task.task_estimated_time,
      task_status: task.task_status,
    },
  };
  var response = await fetch(URL + '/task/update', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function watchAdd(token, task_id) {
  const data = {
    task_id,
  };
  var response = await fetch(URL + '/watch/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function watchCancel(token, task_id) {
  const data = {
    task_id,
  };
  var response = await fetch(URL + '/watch/cancel', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function getUser(token) {
  var response = await fetch(URL + '/task/detail', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function updateUser(token, name) {
  const data = {
    name,
  };
  var response = await fetch(URL + '/task/detail', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function connectionRequest(token, email) {
  const data = {
    email,
  };
  var response = await fetch(URL + '/connection/request', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function connectionReceive(token, email, status) {
  const data = {
    email,
    status,
  };
  var response = await fetch(URL + '/connection/receive', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function getConectionRequests(token) {
  var response = await fetch(URL + '/connection/request/list', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function getConectionList(token, email) {
  var response = await fetch(URL + `/connection/list?email=${email}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function getNotification(token) {
  var response = await fetch(URL + '/notification', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function getWatchList(token, email) {
  var response = await fetch(URL + `/watch/list?email=${email}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function checkWatched(token, task_id) {
  var response = await fetch(URL + `/watch/check?task_id=${task_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function watchTask(token, task_id) {
  const data = { task_id };
  var response = await fetch(URL + `/watch/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function getHistory(token, task_id) {
  var response = await fetch(URL + `/task/history?task_id=${task_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function watchHisotryUpdate(token, task_id) {
  const data = {
    task_id,
  };
  var response = await fetch(URL + `/watch/update`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
    body: JSON.stringify(data),
  });
  return catchError(response);
}

export async function getWorkload(token, email) {
  var response = await fetch(URL + `/workload?email=${email}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}

export async function getRecommended(token) {
  var response = await fetch(URL + `/recommendation`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  });
  return catchError(response);
}
