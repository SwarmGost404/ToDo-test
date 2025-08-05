<template>
  <div 
    class="column"
    @dragover.prevent
    @drop="handleDrop"
  >
    <h2>{{ title }}</h2>
    <div class="tasks">
      <div 
        v-for="task in tasks" 
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
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in-progress' | 'done';
  createdAt: number;
}

export default defineComponent({
  name: 'KanbanColumn',
  props: {
    title: {
      type: String,
      required: true
    },
    status: {
      type: String as PropType<'todo' | 'in-progress' | 'done'>,
      required: true
    },
    tasks: {
      type: Array as PropType<Task[]>,
      required: true
    }
  },
  emits: ['task-dropped', 'task-deleted'],
  setup(props, { emit }) {
    const handleDragStart = (event: DragEvent, taskId: string) => {
      if (event.dataTransfer) {
        event.dataTransfer.setData('taskId', taskId);
      }
    };

    const handleDrop = () => {
      emit('task-dropped', props.status);
    };

    const deleteTask = (taskId: string) => {
      emit('task-deleted', taskId);
    };

    return {
      handleDragStart,
      handleDrop,
      deleteTask
    };
  }
});
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
}

.task {
  background: white;
  border-radius: 6px;
  padding: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: grab;
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