<template>
  <div class="kanban-board">
    <h1>Use your time</h1>
    <TaskForm @add-task="handleAddTask" />
    <div class="columns">
      <KanbanColumn
        v-for="column in columns"
        :key="column.status"
        :column="column"
        :tasks="tasks"
        @task-dropped="handleTaskDrop"
        @delete-task="handleDeleteTask"
      />
    </div>
  </div>
</template>

<script setup lang="ts">

import { useWebSocket } from '../../composables/useWebSocket'
import KanbanColumn from './KanbanColumn.vue'
import TaskForm from './TaskForm.vue'
import type { Task, Column } from '../../models/task'

const columns: Column[] = [
  { title: 'To Do', status: 'todo' },
  { title: 'In Progress', status: 'in-progress' },
  { title: 'Done', status: 'done' },
]

const { tasks, sendMessage, initWebSocket } = useWebSocket()

initWebSocket('ws://localhost:8000/ws')

const handleAddTask = ({ title, description }: { title: string; description: string }) => {
  const newTask: Task = {
    id: Date.now().toString(),
    title,
    description,
    status: 'todo',
    createdAt: Date.now(),
  }
  sendMessage({ type: 'add-task', task: newTask })
}

const handleTaskDrop = (taskId: string, newStatus: Column['status']) => {
  sendMessage({ type: 'move-task', taskId, newStatus })
}

const handleDeleteTask = (taskId: string) => {
  if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
    sendMessage({ type: 'delete-task', taskId })
  }
}
</script>

<style scoped>
.kanban-board {
  padding: 20px;
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.columns {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 768px) {
  .columns {
    grid-template-columns: 1fr;
  }
}
</style>