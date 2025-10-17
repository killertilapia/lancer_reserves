<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-pencil-square me-2"></i>
            Edit Reserve
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
            <!-- General Error Alert -->
            <div v-if="errors.general" class="alert alert-danger" role="alert">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ errors.general }}
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="editReserveId" class="form-label">Reserve ID</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="editReserveId"
                  v-model="form.id"
                  readonly
                  disabled
                >
                <div class="form-text">ID cannot be changed</div>
              </div>
              
              <div class="col-md-6 mb-3">
                <label for="editReserveName" class="form-label">Reserve Name *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="editReserveName"
                  v-model="form.name"
                  :class="{ 'is-invalid': errors.name }"
                  placeholder="Enter reserve name"
                  required
                >
                <div v-if="errors.name" class="invalid-feedback">
                  {{ errors.name }}
                </div>
              </div>
            </div>
            
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="editReserveType" class="form-label">Type *</label>
                <select 
                  class="form-select" 
                  id="editReserveType"
                  v-model="form.type"
                  :class="{ 'is-invalid': errors.type }"
                  required
                >
                  <option value="">Select type</option>
                  <option v-for="option in reserveTypeOptions" :key="option.value" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
                <div v-if="errors.type" class="invalid-feedback">
                  {{ errors.type }}
                </div>
              </div>
              
              <div class="col-md-6 mb-3">
                <label for="editReserveLabel" class="form-label">Label *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="editReserveLabel"
                  v-model="form.label"
                  :class="{ 'is-invalid': errors.label }"
                  placeholder="Enter category label"
                  required
                >
                <div v-if="errors.label" class="invalid-feedback">
                  {{ errors.label }}
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <label for="editReserveDescription" class="form-label">Description *</label>
              <textarea 
                class="form-control" 
                id="editReserveDescription"
                v-model="form.description"
                :class="{ 'is-invalid': errors.description }"
                rows="4"
                placeholder="Enter detailed description (HTML supported)"
                required
              ></textarea>
              <div v-if="errors.description" class="invalid-feedback">
                {{ errors.description }}
              </div>
              <div class="form-text">Detailed description of the reserve. HTML formatting is supported.</div>
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
              {{ isSubmitting ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { RESERVE_TYPES } from '../services/graphql.js'

// Define props
const props = defineProps({
  reserve: {
    type: Object,
    required: true
  }
})

// Define emits
const emit = defineEmits(['close', 'save'])

// Form data
const form = reactive({
  id: '',
  name: '',
  type: '',
  label: '',
  description: ''
})

// Form state
const isSubmitting = ref(false)
const errors = ref({})

// Reserve type options
const reserveTypeOptions = [
  { value: RESERVE_TYPES.BONUS, label: 'Bonus' },
  { value: RESERVE_TYPES.RESOURCE, label: 'Resource' },
  { value: RESERVE_TYPES.MECH, label: 'Mech' },
  { value: RESERVE_TYPES.TACTICAL, label: 'Tactical' }
]

// Initialize form with reserve data
onMounted(() => {
  form.id = props.reserve.id
  form.name = props.reserve.name
  form.type = props.reserve.type
  form.label = props.reserve.label
  form.description = props.reserve.description
})

// Validation
const validateForm = () => {
  errors.value = {}
  
  if (!form.name.trim()) {
    errors.value.name = 'Reserve name is required'
  }
  
  if (!form.type) {
    errors.value.type = 'Reserve type is required'
  }
  
  if (!form.label.trim()) {
    errors.value.label = 'Label is required'
  }
  
  if (!form.description.trim()) {
    errors.value.description = 'Description is required'
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
    // Emit the save event with form data (excluding ID since it can't be changed)
    const updateData = {
      name: form.name,
      type: form.type,
      label: form.label,
      description: form.description
    }
    
    emit('save', form.id, updateData)
  } catch (error) {
    console.error('Error saving reserve:', error)
    errors.value.general = 'Failed to save reserve. Please try again.'
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

.form-control:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
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
