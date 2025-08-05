<template>
  <div class="add-task">
    <input v-model="title" placeholder="Название задачи" @keyup.enter="emitAddTask" />
    <textarea
      v-model="description"
      placeholder="Описание задачи"
      @keyup.enter="emitAddTask"
    ></textarea>
    <button @click="emitAddTask">Добавить задачу</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('')
const description = ref('')

const emit = defineEmits<{
  (e: 'add-task', task: { title: string; description: string }): void
}>()

const emitAddTask = () => {
  if (!title.value.trim()) return
  emit('add-task', { title: title.value, description: description.value })
  title.value = ''
  description.value = ''
}
</script>

<style scoped>
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
}

.add-task button:hover {
  background: #45a049;
}
</style>