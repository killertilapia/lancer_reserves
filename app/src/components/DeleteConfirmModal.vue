<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-danger text-white">
          <h5 class="modal-title">
            <i class="bi bi-exclamation-triangle me-2"></i>
            Confirm Delete
          </h5>
          <button 
            type="button" 
            class="btn-close btn-close-white" 
            @click="$emit('close')"
            aria-label="Close"
          ></button>
        </div>
        
        <div class="modal-body">
          <!-- Error Alert -->
          <div v-if="error" class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ error }}
          </div>

          <div class="text-center mb-3">
            <i class="bi bi-trash fs-1 text-danger"></i>
          </div>

          <p class="mb-3">
            Are you sure you want to delete this reserve? This action cannot be undone.
          </p>

          <div class="card bg-light">
            <div class="card-body">
              <h6 class="card-subtitle mb-2 text-muted">Reserve Details:</h6>
              <p class="mb-1">
                <strong>ID:</strong> <code>{{ reserve.id }}</code>
              </p>
              <p class="mb-1">
                <strong>Name:</strong> {{ reserve.name }}
              </p>
              <p class="mb-0">
                <strong>Type:</strong> 
                <span 
                  class="badge" 
                  :class="{
                    'bg-success': reserve.type === 'BONUS',
                    'bg-warning': reserve.type === 'RESOURCE',
                    'bg-info': reserve.type === 'MECH',
                    'bg-secondary': reserve.type === 'TACTICAL'
                  }"
                >
                  {{ reserve.type }}
                </span>
              </p>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-secondary" 
            @click="$emit('close')"
            :disabled="isDeleting"
          >
            Cancel
          </button>
          <button 
            type="button" 
            class="btn btn-danger"
            @click="handleDelete"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="spinner-border spinner-border-sm me-2" role="status"></span>
            {{ isDeleting ? 'Deleting...' : 'Delete Reserve' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Define props
const props = defineProps({
  reserve: {
    type: Object,
    required: true
  }
})

// Define emits
const emit = defineEmits(['close', 'confirm'])

// State
const isDeleting = ref(false)
const error = ref(null)

// Handle delete confirmation
const handleDelete = async () => {
  isDeleting.value = true
  error.value = null
  
  try {
    emit('confirm', props.reserve.id)
  } catch (err) {
    error.value = 'Failed to delete reserve. Please try again.'
    console.error('Error deleting reserve:', err)
    isDeleting.value = false
  }
}
</script>

<style scoped>
.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
}

.card {
  border: none;
}

.btn {
  border-radius: 0.375rem;
  font-weight: 500;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

code {
  font-size: 0.9em;
  color: #d63384;
}
</style>
