<template>
  <div class="column" @dragover.prevent @drop="handleDrop">
    <h2>{{ column.title }}</h2>
    <div class="tasks">
      <TaskItem
        v-for="task in filteredTasks"
        :key="task.id"
        :task="task"
        @drag-start="emitDragStart"
        @delete-task="emitDeleteTask"
        @open-task="onOpenTask"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import TaskItem from './TaskItem.vue'
import type { Task, Column } from '../../models/task'

const props = defineProps<{
  column: Column
  tasks: Task[]
}>()

const emit = defineEmits<{
  (e: 'task-dropped', taskId: string, newStatus: Column['status']): void
  (e: 'delete-task', taskId: string): void
  (e: 'drag-start', taskId: string): void
  (e: 'open-task', taskId: string): void
}>()

const filteredTasks = computed(() => {
  return props.tasks.filter((task) => task.status === props.column.status)
})

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  const taskId = event.dataTransfer?.getData('text/plain')
  if (taskId) {
    emit('task-dropped', taskId, props.column.status)
  }
}

const emitDeleteTask = (taskId: string) => {
  emit('delete-task', taskId)
}

const emitDragStart = (taskId: string) => {
  emit('drag-start', taskId)
}
const onOpenTask = (taskId: string) => {
  emit('open-task', taskId)
}
</script>

<style scoped>
.column {
  background: #f0f0f0;
  border-radius: 8px;
  padding: 15px;
  min-height: 400px;
}

h2 {
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
</style>