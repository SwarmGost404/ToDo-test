<template>
  <div class="task" draggable="true" @dragstart="handleDragStart">
    <div class="task-header">
      <h3>{{ task.title }}</h3>
      <button class="delete-btn" @click="emitDeleteTask">×</button>
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
}>()

const handleDragStart = (event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', props.task.id)
    emit('drag-start', props.task.id)
    event.dataTransfer.effectAllowed = 'move'
  }
}

const emitDeleteTask = () => {
  emit('delete-task', props.task.id)
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
</style>