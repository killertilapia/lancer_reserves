<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-danger text-white">
          <h5 class="modal-title">
            <i class="bi bi-exclamation-triangle me-2"></i>
            Confirm Delete Reserve
          </h5>
          <button 
            type="button" 
            class="btn-close btn-close-white" 
            @click="$emit('close')"
            aria-label="Close"
          ></button>
        </div>
        
        <div class="modal-body">
          <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Warning:</strong> This action cannot be undone!
          </div>
          
          <p class="mb-3">Are you sure you want to delete this reserve?</p>
          
          <div class="card">
            <div class="card-body">
              <dl class="row mb-0">
                <dt class="col-sm-3">ID:</dt>
                <dd class="col-sm-9">
                  <code>{{ reserve.id }}</code>
                </dd>
                
                <dt class="col-sm-3">Name:</dt>
                <dd class="col-sm-9">{{ reserve.name }}</dd>
                
                <dt class="col-sm-3">Type:</dt>
                <dd class="col-sm-9">
                  <span class="badge bg-secondary">{{ reserve.type }}</span>
                </dd>
                
                <dt class="col-sm-3">Label:</dt>
                <dd class="col-sm-9">{{ reserve.label }}</dd>
              </dl>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-secondary" 
            @click="$emit('close')"
          >
            <i class="bi bi-x-circle me-1"></i>
            Cancel
          </button>
          <button 
            type="button" 
            class="btn btn-danger"
            @click="confirmDelete"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="spinner-border spinner-border-sm me-2" role="status"></span>
            <i v-else class="bi bi-trash me-1"></i>
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

// Confirm deletion
const confirmDelete = async () => {
  isDeleting.value = true
  
  try {
    // Emit the confirm event with reserve ID
    emit('confirm', props.reserve.id)
  } catch (error) {
    console.error('Error confirming delete:', error)
  } finally {
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
  border: 1px solid #dee2e6;
  background-color: #f8f9fa;
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
  color: #d63384;
  background-color: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

dl {
  margin-bottom: 0;
}

dt {
  font-weight: 600;
}

dd {
  margin-bottom: 0.5rem;
}

dd:last-child {
  margin-bottom: 0;
}
</style>

