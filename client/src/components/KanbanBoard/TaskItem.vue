<template>
  <div class="task" draggable="true"  @dragstart="handleDragStart">
    <div class="task-header">
      <h3>{{ task.title }}</h3>
      <button class="delete-btn" @click="emitDeleteTask">×</button>
      <button class="edith-btn">
        <svg width="24" height="24" @click="emitEdithTask" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M20.71 7.04c.39-.39.39-1.04 0-1.41l-2.34-2.34c-.37-.39-1.02-.39-1.41 0l-1.84 1.83 3.75 3.75 1.84-1.83z" fill="#4285F4"/>
          <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z" fill="#34A853"/>
          <path d="M20.71 7.04l-2.34-2.34c-.37-.39-1.02-.39-1.41 0l-1.84 1.83 3.75 3.75 1.84-1.83c.39-.38.39-1.02 0-1.41z" fill="#FBBC05"/>
          <path d="M17.81 9.94l-3.75-3.75L3 17.25V21h3.75L17.81 9.94z" fill="#EA4335"/>
        </svg>
      </button>
    </div>
    <p>{{ task.description }}</p>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '../../models/task'

const props = defineProps<{
  task: Task
}>()

const emit = defineEmits<{
  (e: 'drag-start', taskId: string): void
  (e: 'delete-task', taskId: string): void
  (e: 'open-task', taskId: string): void

}>()

const handleDragStart = (event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', props.task.id)
    emit('drag-start', props.task.id)
    event.dataTransfer.effectAllowed = 'move'
  }
}

const emitDeleteTask = (): void => {
  emit('delete-task', props.task.id)
}

const emitEdithTask = (): void => {
  emit('open-task', props.task.id)
  console.log(props.task.id)
}
</script>

<style scoped>
.task {
  background: white;
  border-radius: 6px;
  padding: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: grab;
}
.task:hover{
  button {
    display: block;
  }
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
  display: none;
}
.edith-btn {
  background: white;
  border: none;
  display: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
}
.edith-btn:hover,
.delete-btn:hover {
  transform: scale(1.1);
}
</style>