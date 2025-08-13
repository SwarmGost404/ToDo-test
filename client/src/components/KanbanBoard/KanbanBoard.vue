<template>
  <div class="kanban-board">
    <h1>Use your time</h1>
    
    <div class="columns">
      <KanbanColumn
        v-for="column in columns"
        :key="column.status"
        :column="column"
        :tasks="tasks"
        @task-dropped="handleTaskDrop"
        @delete-task="handleDeleteTask"
        @open-task="handleOpenTask"
        @edit-task="handleEditTask(showTask!)"
        @set-color-task="onSetColotTask"
      />
    </div>
    <TaskForm @add-task="handleAddTask" />
  </div>
    <ModalWindow 
      :title="showTask?.title || ''"
      :isOpen="showTask !== null"
      :color="showTask?.color"
      @close="showTask = null"
    >
      <p>{{ showTask?.description }}</p>
      <template #footer>
        <button class="edit-btn-in-modal" @click="handleEditTask(showTask!)">Редактировать</button>
      </template>
    </ModalWindow>
    <ModalWindow 
      title="Редактировать задачу"
      :isOpen="showEditModal"
      @close="showEditModal = false"
      @confirm="handleConfirmEdit"
    >
      <div class="edit-form">
        <input v-model="editingTask.title" type="text" placeholder="Название">
        <textarea v-model="editingTask.description" placeholder="Описание"></textarea>
      </div>
    </ModalWindow>
</template>

<script setup lang="ts">
import ModalWindow from './ModalWindow.vue'
import { useWebSocket } from '../../composables/useWebSocket'
import KanbanColumn from './KanbanColumn.vue'
import TaskForm from './TaskForm.vue'
import type { Task, Column } from '../../models/task'
import { ref } from 'vue'

const columns: Column[] = [
  { title: 'To Do', status: 'todo' },
  { title: 'In Progress', status: 'in-progress' },
  { title: 'Done', status: 'done' },
]

const { tasks, sendMessage, initWebSocket } = useWebSocket()
const showTask = ref<Task|null>(null)
const showEditModal = ref(false)
const editingTask = ref<Partial<Task>>({
  title: '',
  description: ''
})

  
initWebSocket('ws://localhost:8000/ws')

const handleAddTask = ({ title, description }: { title: string; description: string }) => {
  const newTask: Task = {
    id: Date.now().toString(),
    title,
    description,
    status: 'todo',
    createdAt: Date.now(),
    color: 'none-status'
  }
  sendMessage({ type: 'add-task', task: newTask })
}

const handleTaskDrop = (taskId: string, newStatus: Column['status']) => {
  sendMessage({ type: 'move-task', taskId, newStatus })
}

const handleDeleteTask = (taskId: string) => {

  sendMessage({ type: 'delete-task', taskId })

}

const handleConfirmEdit = () => {
  if (editingTask.value.id) {
    sendMessage({
      type: 'edit-task',
      taskId: editingTask.value.id,
      updates: {
        title: editingTask.value.title,
        description: editingTask.value.description
      }
    })
  }
  showEditModal.value = false
}

const handleOpenTask = (taskId: string) => {
  const task = tasks.value.find(t => t.id === taskId)
  
  if (task) {
    showTask.value = { ...task }
  } else {
    console.error('Задача не найдена:', taskId)
  }
}

const handleEditTask = (task: Task) => {
  editingTask.value = { ...task }
  showEditModal.value = true
  showTask.value = null
}

const onSetColotTask = (taskId: string, color: string) => {
  sendMessage({
    type: 'edit-task',
    taskId: taskId,
    updates: {
      color: color
    }
  })
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
  margin-bottom: 50px;
}

@media (max-width: 768px) {
  .columns {
    grid-template-columns: 1fr;
  }
}


.edit-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  
  input, textarea {
    padding: 12px 15px;
    border: 2px solid #ff9ff3;
    border-radius: 15px;
    background-color: #fafafa;
    color: #000;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    
    &:focus {
      outline: none;
      border-color: #f368e0;
      box-shadow: 0 0 0 3px rgba(255, 159, 243, 0.3);
    }
  }
  
  textarea {
    min-height: 100px;
    resize: vertical;
  }
  
  position: relative;
  
  &::before {
    content: "✏️";
    position: absolute;
    top: -15px;
    right: -15px;
    font-size: 24px;
    transform: rotate(15deg);
  }
}
.edit-btn-in-modal {
  padding: 12px 15px;
  border: 3px solid #ff9ff3;
  border-radius: 15px;
  background-color: #fafafa;
  color: #000;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

}
</style>