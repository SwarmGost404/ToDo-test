import { ref, onUnmounted } from 'vue'
import type { Task } from '../models/task'

export function useWebSocket() {
  const tasks = ref<Task[]>([])
  const socket = ref<WebSocket | null>(null)

  const initWebSocket = (url: string) => {
    socket.value = new WebSocket(url)

    socket.value.onopen = () => {
      console.log('WebSocket connected')
    }

    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'initial-data') {
        tasks.value = data.tasks
      } else if (data.type === 'task-added') {
        tasks.value.push(data.task)
      } else if (data.type === 'task-moved') {
        const taskIndex = tasks.value.findIndex((t) => t.id === data.taskId)
        if (taskIndex !== -1) {
          tasks.value[taskIndex].status = data.newStatus
        }
      } else if (data.type === 'task-deleted') {
        tasks.value = tasks.value.filter((t) => t.id !== data.taskId)
      }
    }

    socket.value.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    socket.value.onclose = () => {
      console.log('WebSocket disconnected')
      setTimeout(() => initWebSocket(url), 5000)
    }
  }

  const sendMessage = (message: object) => {
    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify(message))
    }
  }

  onUnmounted(() => {
    if (socket.value) {
      socket.value.close()
    }
  })

  return { tasks, sendMessage, initWebSocket }
}