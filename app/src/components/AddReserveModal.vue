<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-plus-circle me-2"></i>
            Add New Reserve
          </h5>
          <button 
            type="button" 
            class="btn-close" 
            @click="$emit('close')"
            aria-label="Close"
          ></button>
        </div>
        
        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="reserveName" class="form-label">Reserve Name *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="reserveName"
                  v-model="form.name"
                  :class="{ 'is-invalid': errors.name }"
                  placeholder="Enter reserve name"
                  required
                >
                <div v-if="errors.name" class="invalid-feedback">
                  {{ errors.name }}
                </div>
              </div>
              
              <div class="col-md-6 mb-3">
                <label for="reserveType" class="form-label">Type *</label>
                <select 
                  class="form-select" 
                  id="reserveType"
                  v-model="form.type"
                  :class="{ 'is-invalid': errors.type }"
                  required
                >
                  <option value="">Select type</option>
                  <option value="Financial">Financial</option>
                  <option value="Physical">Physical</option>
                  <option value="Human">Human</option>
                  <option value="Technical">Technical</option>
                </select>
                <div v-if="errors.type" class="invalid-feedback">
                  {{ errors.type }}
                </div>
              </div>
            </div>
            
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="reserveStatus" class="form-label">Status *</label>
                <select 
                  class="form-select" 
                  id="reserveStatus"
                  v-model="form.status"
                  :class="{ 'is-invalid': errors.status }"
                  required
                >
                  <option value="">Select status</option>
                  <option value="active">Active</option>
                  <option value="pending">Pending</option>
                  <option value="inactive">Inactive</option>
                </select>
                <div v-if="errors.status" class="invalid-feedback">
                  {{ errors.status }}
                </div>
              </div>
              
              <div class="col-md-6 mb-3">
                <label for="reservePriority" class="form-label">Priority</label>
                <select 
                  class="form-select" 
                  id="reservePriority"
                  v-model="form.priority"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
            </div>
            
            <div class="mb-3">
              <label for="reserveDescription" class="form-label">Description</label>
              <textarea 
                class="form-control" 
                id="reserveDescription"
                v-model="form.description"
                rows="3"
                placeholder="Enter reserve description"
              ></textarea>
            </div>
            
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="reserveCapacity" class="form-label">Capacity</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="reserveCapacity"
                  v-model.number="form.capacity"
                  placeholder="Enter capacity"
                  min="0"
                >
              </div>
              
              <div class="col-md-6 mb-3">
                <label for="reserveLocation" class="form-label">Location</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="reserveLocation"
                  v-model="form.location"
                  placeholder="Enter location"
                >
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-secondary" 
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
              {{ isSubmitting ? 'Saving...' : 'Save Reserve' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// Define emits
const emit = defineEmits(['close', 'save'])

// Form data
const form = reactive({
  name: '',
  type: '',
  status: '',
  priority: 'medium',
  description: '',
  capacity: null,
  location: ''
})

// Form state
const isSubmitting = ref(false)
const errors = ref({})

// Validation
const validateForm = () => {
  errors.value = {}
  
  if (!form.name.trim()) {
    errors.value.name = 'Reserve name is required'
  }
  
  if (!form.type) {
    errors.value.type = 'Reserve type is required'
  }
  
  if (!form.status) {
    errors.value.status = 'Reserve status is required'
  }
  
  return Object.keys(errors.value).length === 0
}

// Handle form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Emit the save event with form data
    emit('save', { ...form })
    
    // Reset form
    Object.keys(form).forEach(key => {
      if (key === 'priority') {
        form[key] = 'medium'
      } else {
        form[key] = ''
      }
    })
    
  } catch (error) {
    console.error('Error saving reserve:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.modal-content {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.form-label {
  font-weight: 600;
  color: #495057;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn {
  border-radius: 0.375rem;
  font-weight: 500;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
