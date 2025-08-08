<template>
  <transition name="modal">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="close-button" @click="closeModal">&times;</button>
        </div>
        
        <div class="modal-content">
          <slot></slot>
        </div>
        
        <div class="modal-footer">
          <slot name="footer">
            <button class="cancel-button" @click="closeModal">Отмена</button>
            <button class="confirm-button" @click="confirmAction">Подтвердить</button>
          </slot>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">

const props = defineProps({
  title: {
    type: String,
    default: 'Модальное окно'
  },
  isOpen: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'confirm'): void
}>();

const closeModal = () => {
  emit('close');
};

const confirmAction = () => {
  emit('confirm');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  color: #000;
  
}

.modal-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-content {
  padding: 20px;
  overflow-y: auto;
  flex-grow: 1;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.cancel-button, .confirm-button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-button {
  background: #f0f0f0;
  border: 1px solid #ddd;
}

.confirm-button {
  background: #42b983;
  color: white;
  border: none;
}

/* Анимации */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: translateY(-20px);
}
</style>