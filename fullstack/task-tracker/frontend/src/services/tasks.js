import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_TASK_API_BASE_URL || 'http://localhost:8002'

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export async function fetchTasks(status = null) {
  const params = status ? { status } : {}
  const response = await client.get('/tasks', { params })
  return response.data
}

export async function getTask(taskId) {
  const response = await client.get(`/tasks/${taskId}`)
  return response.data
}

export async function createTask(payload) {
  const response = await client.post('/tasks', payload)
  return response.data
}

export async function updateTask(taskId, payload) {
  const response = await client.patch(`/tasks/${taskId}`, payload)
  return response.data
}

export async function updateTaskStatus(taskId, status) {
  const response = await client.patch(`/tasks/${taskId}/status`, { status })
  return response.data
}

export async function deleteTask(taskId) {
  await client.delete(`/tasks/${taskId}`)
}
