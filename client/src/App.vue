<template>
  <div class="kanban-board">
    <h1>Канбан-доска (режим реального времени)</h1>

    <div class="add-task">
      <input v-model="newTaskTitle" placeholder="Название задачи" @keyup.enter="addTask" />
      <textarea
        v-model="newTaskDescription"
        placeholder="Описание задачи"
        @keyup.enter="addTask"
      ></textarea>
      <button @click="addTask">Добавить задачу</button>
    </div>

    <div class="columns">
      <div
        v-for="column in columns"
        :key="column.status"
        class="column"
        @dragover.prevent
        @drop="handleDrop($event, column.status)"
      >
        <h2>{{ column.title }}</h2>
        <div class="tasks">
          <div
            v-for="task in filteredTasks(column.status)"
            :key="task.id"
            class="task"
            draggable="true"
            @dragstart="handleDragStart($event, task.id)"
          >
            <div class="task-header">
              <h3>{{ task.title }}</h3>
              <button class="delete-btn" @click="deleteTask(task.id)">×</button>
            </div>
            <p>{{ task.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted, onUnmounted } from 'vue'

  interface Task {
    id: string
    title: string
    description: string
    status: 'todo' | 'in-progress' | 'done'
    createdAt: number
  }

  interface Column {
    title: string
    status: 'todo' | 'in-progress' | 'done'
  }

  export default defineComponent({
    name: 'App',
    setup() {
      const columns: Column[] = [
        { title: 'To Do', status: 'todo' },
        { title: 'In Progress', status: 'in-progress' },
        { title: 'Done', status: 'done' },
      ]

      const tasks = ref<Task[]>([])
      const newTaskTitle = ref('')
      const newTaskDescription = ref('')
      const socket = ref<WebSocket | null>(null)
      const draggedTaskId = ref<string | null>(null)

      // Фильтрация задач по статусу
      const filteredTasks = (status: string) => {
        return tasks.value.filter((task) => task.status === status)
      }

      // Добавление новой задачи
      const addTask = () => {
        if (!newTaskTitle.value.trim()) return

        const newTask: Task = {
          id: Date.now().toString(),
          title: newTaskTitle.value,
          description: newTaskDescription.value,
          status: 'todo',
          createdAt: Date.now(),
        }

        if (socket.value?.readyState === WebSocket.OPEN) {
          socket.value.send(
            JSON.stringify({
              type: 'add-task',
              task: newTask,
            })
          )
        }

        newTaskTitle.value = ''
        newTaskDescription.value = ''
      }

      // Начало перетаскивания
      const handleDragStart = (event: DragEvent, taskId: string) => {
        if (event.dataTransfer) {
          event.dataTransfer.setData('text/plain', taskId)
          draggedTaskId.value = taskId
          event.dataTransfer.effectAllowed = 'move'
        }
      }

      // Обработка события drop
      const handleDrop = (event: DragEvent, newStatus: 'todo' | 'in-progress' | 'done') => {
        event.preventDefault()
        const taskId = event.dataTransfer?.getData('text/plain')
        if (taskId) {
          moveTask(taskId, newStatus)
        }
      }

      // Перемещение задачи между колонками
      const moveTask = (taskId: string, newStatus: 'todo' | 'in-progress' | 'done') => {
        if (socket.value?.readyState === WebSocket.OPEN) {
          socket.value.send(
            JSON.stringify({
              type: 'move-task',
              taskId,
              newStatus,
            })
          )
        }
      }

      // Удаление задачи
      const deleteTask = (taskId: string) => {
        if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
          if (socket.value?.readyState === WebSocket.OPEN) {
            socket.value.send(
              JSON.stringify({
                type: 'delete-task',
                taskId,
              })
            )
          }
        }
      }

      // Инициализация WebSocket
      const initWebSocket = () => {
        const wsUrl = 'ws://192.168.1.71:8000/ws'
        socket.value = new WebSocket(wsUrl)

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
          setTimeout(initWebSocket, 5000)
        }
      }

      onMounted(() => {
        initWebSocket()
      })

      onUnmounted(() => {
        if (socket.value) {
          socket.value.close()
        }
      })

      return {
        columns,
        tasks,
        newTaskTitle,
        newTaskDescription,
        filteredTasks,
        addTask,
        handleDragStart,
        handleDrop,
        deleteTask,
      }
    },
  })
</script>

<style scoped>
  /* Стили остаются без изменений */
  .kanban-board {
    padding: 20px;
    font-family: Arial, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
  }

  h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }

  .add-task {
    margin-bottom: 30px;
    padding: 15px;
    background: #f5f5f5;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .add-task input,
  .add-task textarea {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }

  .add-task textarea {
    min-height: 60px;
    resize: vertical;
  }

  .add-task button {
    padding: 10px 15px;
    background: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
  }

  .add-task button:hover {
    background: #45a049;
  }

  .columns {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }

  .column {
    background: #f0f0f0;
    border-radius: 8px;
    padding: 15px;
    min-height: 400px;
  }

  .column h2 {
    margin-top: 0;
    color: #333;
    border-bottom: 2px solid #ddd;
    padding-bottom: 10px;
  }

  .tasks {
    display: flex;
    flex-direction: column;
    gap: 15px;
    min-height: 300px;
  }

  .task {
    background: white;
    border-radius: 6px;
    padding: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    cursor: grab;
  }

  .task:active {
    cursor: grabbing;
  }

  .task-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .task h3 {
    margin: 0;
    font-size: 16px;
    color: #444;
  }

  .task p {
    margin: 0;
    font-size: 14px;
    color: #666;
  }

  .delete-btn {
    background: #ff4444;
    color: white;
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  }

  .delete-btn:hover {
    background: #cc0000;
  }

  @media (max-width: 768px) {
    .columns {
      grid-template-columns: 1fr;
    }
  }
</style>
