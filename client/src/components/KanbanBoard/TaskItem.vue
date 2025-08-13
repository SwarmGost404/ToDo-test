<template>
  <div class="task" :class="props.task.color" draggable="true" @click="emitOpenTask" @dragstart="handleDragStart">
    <div class="task-header">
      <h3>{{ task.title }}</h3>
      <div class="task-hovered-button">
        <button class="delete-btn" @click="emitDeleteTask" @click.stop="emitDeleteTask">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            <line x1="10" y1="11" x2="10" y2="17"/>
            <line x1="14" y1="11" x2="14" y2="17"/>
          </svg>
        </button>
        <button @click="emitEdithTask"  class="edith-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 19l7-7 3 3-7 7-3-3z"/>
            <path d="M18 13l-1.5-1.5L4 2 2 4l9.5 9.5L13 18z"/>
          </svg>
        </button>
        <button class="set-color-btn" @click.stop="isHovered = !isHovered">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12" y2="16"/>
          </svg>
        </button>
        
      </div>
      
    </div>
    <div class="hovered-color-panel" v-if="isHovered">
      <button class="color-button status-red" @click.stop="handleSetColorTask('status-red')"></button>
      <button class="color-button status-green" @click.stop="handleSetColorTask('status-green')"></button>
      <button class="color-button status-yellow" @click.stop="handleSetColorTask('status-yellow')"></button>
      <button class="color-button status-none" @click.stop="handleSetColorTask('status-none')"></button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '../../models/task'
import { ref } from 'vue';

const isHovered = ref<boolean>(false)

const props = defineProps<{
  task: Task
}>()

const emit = defineEmits<{
  (e: 'drag-start', taskId: string): void
  (e: 'delete-task', taskId: string): void
  (e: 'open-task', taskId: string): void
  (e: 'set-color-task', taskID: string, color: string): void
  (e: 'edit-task', task: Task): void
}>()

const handleDragStart = (event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', props.task.id)
    emit('drag-start', props.task.id)
    event.dataTransfer.effectAllowed = 'move'
  }
}

const emitOpenTask = (): void => {
  emit('open-task', props.task.id)
}

const emitDeleteTask = (): void => {
  emit('delete-task', props.task.id)
}

const emitEdithTask = (): void => {
  emit('edit-task', props.task)
}
const handleSetColorTask = (color: string): void => {
  emit('set-color-task', props.task.id, color)
}
</script>

<style scoped>
.task {
  border: 3px solid #000;
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: grab;
  
}

.task:hover{
  .task-hovered-button {
    display: flex;
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
  color: #000;
  width: 60%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-hovered-button {
  display: none;
  margin-right: 10px;
  button {
    background-color: transparent;
    border: none;
    width: 24px;
    height: 24px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: black;
    margin-right: 10px;
  }
  button:hover {
    transform: scale(1.1);
  }
}

.color-button {
  width: 24px;
  height: 24px;
  border: 3px solid #000;
  border-radius: 50%;
}

.status-red {
  background-color: rgb(255, 80, 80);
}

.status-green {
  background-color: rgb(73, 255, 73);
}

.status-yellow {
  background-color: rgb(255, 255, 95);
}

.status-none {
  background-color: #fff;
}

</style>