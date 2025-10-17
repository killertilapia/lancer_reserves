<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-plus-circle me-2"></i>
            Add New Lancer Reserve
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
            <!-- Basic Information -->
            <div class="row mb-4">
              <div class="col-12">
                <h6 class="text-primary border-bottom pb-2">
                  <i class="bi bi-info-circle me-2"></i>
                  Basic Information
                </h6>
              </div>
            </div>
            
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="reserveId" class="form-label">Reserve ID *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="reserveId"
                  v-model="form.id"
                  readonly
                  placeholder="Auto-generated"
                >
                <div class="form-text">This ID is automatically generated</div>
              </div>
              
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
            </div>
            
            <div class="row">
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
                  <option value="Bonus">Bonus</option>
                  <option value="Resource">Resource</option>
                  <option value="Mech">Mech</option>
                  <option value="Tactical">Tactical</option>
                </select>
                <div v-if="errors.type" class="invalid-feedback">
                  {{ errors.type }}
                </div>
              </div>
              
              <div class="col-md-6 mb-3">
                <label for="reserveLabel" class="form-label">Label *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="reserveLabel"
                  v-model="form.label"
                  :class="{ 'is-invalid': errors.label }"
                  placeholder="Enter reserve label"
                  required
                >
                <div v-if="errors.label" class="invalid-feedback">
                  {{ errors.label }}
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <label for="reserveDescription" class="form-label">Description *</label>
              <textarea 
                class="form-control" 
                id="reserveDescription"
                v-model="form.description"
                :class="{ 'is-invalid': errors.description }"
                rows="3"
                placeholder="Enter reserve description"
                required
              ></textarea>
              <div v-if="errors.description" class="invalid-feedback">
                {{ errors.description }}
              </div>
            </div>

            <!-- Bonuses Section -->
            <div class="row mb-4">
              <div class="col-12">
                <h6 class="text-primary border-bottom pb-2">
                  <i class="bi bi-star me-2"></i>
                  Bonuses
                </h6>
              </div>
            </div>
            
            <div v-for="(bonus, index) in form.bonuses" :key="`bonus-${index}`" class="row mb-3">
              <div class="col-md-5">
                <label :for="`bonusId-${index}`" class="form-label">Bonus ID</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :id="`bonusId-${index}`"
                  v-model="bonus.id"
                  placeholder="e.g., accuracy, damage"
                >
              </div>
              <div class="col-md-5">
                <label :for="`bonusVal-${index}`" class="form-label">Value</label>
                <input 
                  type="number" 
                  class="form-control" 
                  :id="`bonusVal-${index}`"
                  v-model.number="bonus.val"
                  placeholder="e.g., 1, 2, 3"
                >
              </div>
              <div class="col-md-2 d-flex align-items-end">
                <button 
                  type="button" 
                  class="btn btn-outline-danger btn-sm"
                  @click="removeBonus(index)"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            
            <div class="mb-3">
              <button 
                type="button" 
                class="btn btn-outline-primary btn-sm"
                @click="addBonus"
              >
                <i class="bi bi-plus-circle me-1"></i>
                Add Bonus
              </button>
            </div>

            <!-- Deployables Section -->
            <div class="row mb-4">
              <div class="col-12">
                <h6 class="text-primary border-bottom pb-2">
                  <i class="bi bi-box me-2"></i>
                  Deployables
                </h6>
              </div>
            </div>
            
            <div v-for="(deployable, index) in form.deployables" :key="`deployable-${index}`" class="row mb-3">
              <div class="col-md-3">
                <label :for="`deployableName-${index}`" class="form-label">Name</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :id="`deployableName-${index}`"
                  v-model="deployable.name"
                  placeholder="Deployable name"
                >
              </div>
              <div class="col-md-2">
                <label :for="`deployableType-${index}`" class="form-label">Type</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :id="`deployableType-${index}`"
                  v-model="deployable.type"
                  placeholder="Type"
                >
              </div>
              <div class="col-md-2">
                <label :for="`deployableSize-${index}`" class="form-label">Size</label>
                <input 
                  type="number" 
                  class="form-control" 
                  :id="`deployableSize-${index}`"
                  v-model.number="deployable.size"
                  placeholder="Size"
                >
              </div>
              <div class="col-md-4">
                <label :for="`deployableDetail-${index}`" class="form-label">Detail</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :id="`deployableDetail-${index}`"
                  v-model="deployable.detail"
                  placeholder="Details"
                >
              </div>
              <div class="col-md-1 d-flex align-items-end">
                <button 
                  type="button" 
                  class="btn btn-outline-danger btn-sm"
                  @click="removeDeployable(index)"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            
            <div class="mb-3">
              <button 
                type="button" 
                class="btn btn-outline-primary btn-sm"
                @click="addDeployable"
              >
                <i class="bi bi-plus-circle me-1"></i>
                Add Deployable
              </button>
            </div>

            <!-- Actions Section -->
            <div class="row mb-4">
              <div class="col-12">
                <h6 class="text-primary border-bottom pb-2">
                  <i class="bi bi-lightning me-2"></i>
                  Actions
                </h6>
              </div>
            </div>
            
            <div v-for="(action, index) in form.actions" :key="`action-${index}`" class="mb-4">
              <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <span>Action {{ index + 1 }}</span>
                  <button 
                    type="button" 
                    class="btn btn-outline-danger btn-sm"
                    @click="removeAction(index)"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
                <div class="card-body">
                  <div class="row mb-3">
                    <div class="col-md-4">
                      <label :for="`actionName-${index}`" class="form-label">Name</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        :id="`actionName-${index}`"
                        v-model="action.name"
                        placeholder="Action name"
                      >
                    </div>
                    <div class="col-md-4">
                      <label :for="`actionActivation-${index}`" class="form-label">Activation</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        :id="`actionActivation-${index}`"
                        v-model="action.activation"
                        placeholder="e.g., Quick, Full"
                      >
                    </div>
                    <div class="col-md-4">
                      <label :for="`actionDetail-${index}`" class="form-label">Detail</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        :id="`actionDetail-${index}`"
                        v-model="action.detail"
                        placeholder="Action details"
                      >
                    </div>
                  </div>
                  
                  <!-- Range -->
                  <div class="mb-3">
                    <label class="form-label">Range</label>
                    <div v-for="(range, rangeIndex) in action.range" :key="`range-${index}-${rangeIndex}`" class="row mb-2">
                      <div class="col-md-6">
                        <input 
                          type="text" 
                          class="form-control" 
                          v-model="range.type"
                          placeholder="Range type"
                        >
                      </div>
                      <div class="col-md-4">
                        <input 
                          type="number" 
                          class="form-control" 
                          v-model.number="range.val"
                          placeholder="Value"
                        >
                      </div>
                      <div class="col-md-2">
                        <button 
                          type="button" 
                          class="btn btn-outline-danger btn-sm"
                          @click="removeRange(index, rangeIndex)"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                    <button 
                      type="button" 
                      class="btn btn-outline-secondary btn-sm"
                      @click="addRange(index)"
                    >
                      <i class="bi bi-plus-circle me-1"></i>
                      Add Range
                    </button>
                  </div>
                  
                  <!-- Damage -->
                  <div class="mb-3">
                    <label class="form-label">Damage</label>
                    <div v-for="(damage, damageIndex) in action.damage" :key="`damage-${index}-${damageIndex}`" class="row mb-2">
                      <div class="col-md-6">
                        <input 
                          type="text" 
                          class="form-control" 
                          v-model="damage.type"
                          placeholder="Damage type"
                        >
                      </div>
                      <div class="col-md-4">
                        <input 
                          type="text" 
                          class="form-control" 
                          v-model="damage.val"
                          placeholder="Value"
                        >
                      </div>
                      <div class="col-md-2">
                        <button 
                          type="button" 
                          class="btn btn-outline-danger btn-sm"
                          @click="removeDamage(index, damageIndex)"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                    <button 
                      type="button" 
                      class="btn btn-outline-secondary btn-sm"
                      @click="addDamage(index)"
                    >
                      <i class="bi bi-plus-circle me-1"></i>
                      Add Damage
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <button 
                type="button" 
                class="btn btn-outline-primary btn-sm"
                @click="addAction"
              >
                <i class="bi bi-plus-circle me-1"></i>
                Add Action
              </button>
            </div>

            <!-- Synergies Section -->
            <div class="row mb-4">
              <div class="col-12">
                <h6 class="text-primary border-bottom pb-2">
                  <i class="bi bi-link me-2"></i>
                  Synergies
                </h6>
              </div>
            </div>
            
            <div v-for="(synergy, index) in form.synergies" :key="`synergy-${index}`" class="row mb-3">
              <div class="col-md-5">
                <label :for="`synergyLocations-${index}`" class="form-label">Locations</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :id="`synergyLocations-${index}`"
                  v-model="synergy.locationsText"
                  placeholder="Comma-separated locations"
                >
                <div class="form-text">Enter locations separated by commas</div>
              </div>
              <div class="col-md-6">
                <label :for="`synergyDetail-${index}`" class="form-label">Detail</label>
                <input 
                  type="text" 
                  class="form-control" 
                  :id="`synergyDetail-${index}`"
                  v-model="synergy.detail"
                  placeholder="Synergy details"
                >
              </div>
              <div class="col-md-1 d-flex align-items-end">
                <button 
                  type="button" 
                  class="btn btn-outline-danger btn-sm"
                  @click="removeSynergy(index)"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
              <div class="form-text">Detailed description of the reserve. HTML formatting is supported.</div>
            </div>
            
            <div class="mb-3">
              <button 
                type="button" 
                class="btn btn-outline-primary btn-sm"
                @click="addSynergy"
              >
                <i class="bi bi-plus-circle me-1"></i>
                Add Synergy
              </button>
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
import { ref, reactive, onMounted } from 'vue'
import { generateReserveId } from '../services/graphql.js'

// Define emits
const emit = defineEmits(['close', 'save'])

// Form data
const form = reactive({
  id: '',
  name: '',
  type: '',
  label: '',
  description: '',
  bonuses: [],
  deployables: [],
  actions: [],
  synergies: []
})

// Form state
const isSubmitting = ref(false)
const errors = ref({})

// Initialize form with generated ID
onMounted(() => {
  form.id = generateReserveId()
})

// Validation
const validateForm = () => {
  errors.value = {}
  
  if (!form.id.trim()) {
    errors.value.id = 'Reserve ID is required'
  } else if (!/^[a-zA-Z0-9_-]+$/.test(form.id)) {
    errors.value.id = 'ID can only contain letters, numbers, underscores, and hyphens'
  }
  
  if (!form.name.trim()) {
    errors.value.name = 'Reserve name is required'
  }
  
  if (!form.type) {
    errors.value.type = 'Reserve type is required'
  }
  
  if (!form.label.trim()) {
    errors.value.label = 'Reserve label is required'
  }
  
  if (!form.description.trim()) {
    errors.value.description = 'Reserve description is required'
  }
  
  return Object.keys(errors.value).length === 0
}

// Bonus management
const addBonus = () => {
  form.bonuses.push({ id: '', val: 0 })
}

const removeBonus = (index) => {
  form.bonuses.splice(index, 1)
}

// Deployable management
const addDeployable = () => {
  form.deployables.push({ name: '', type: '', size: 0, detail: '' })
}

const removeDeployable = (index) => {
  form.deployables.splice(index, 1)
}

// Action management
const addAction = () => {
  form.actions.push({
    name: '',
    activation: '',
    detail: '',
    range: [],
    damage: []
  })
}

const removeAction = (index) => {
  form.actions.splice(index, 1)
}

const addRange = (actionIndex) => {
  form.actions[actionIndex].range.push({ type: '', val: 0 })
}

const removeRange = (actionIndex, rangeIndex) => {
  form.actions[actionIndex].range.splice(rangeIndex, 1)
}

const addDamage = (actionIndex) => {
  form.actions[actionIndex].damage.push({ type: '', val: '' })
}

const removeDamage = (actionIndex, damageIndex) => {
  form.actions[actionIndex].damage.splice(damageIndex, 1)
}

// Synergy management
const addSynergy = () => {
  form.synergies.push({ locationsText: '', detail: '' })
}

const removeSynergy = (index) => {
  form.synergies.splice(index, 1)
}

// Transform form data for GraphQL
const transformFormData = () => {
  const transformed = {
    id: form.id,
    name: form.name,
    type: form.type,
    label: form.label,
    description: form.description,
    bonuses: form.bonuses.filter(b => b.id.trim() && b.val !== null),
    deployables: form.deployables.filter(d => d.name.trim()),
    actions: form.actions.filter(a => a.name.trim()).map(action => ({
      name: action.name,
      activation: action.activation,
      detail: action.detail,
      range: action.range.filter(r => r.type.trim()),
      damage: action.damage.filter(d => d.type.trim())
    })),
    synergies: form.synergies.filter(s => s.detail.trim()).map(synergy => ({
      locations: synergy.locationsText.split(',').map(loc => loc.trim()).filter(loc => loc),
      detail: synergy.detail
    }))
  }
  
  return transformed
}

// Handle form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  isSubmitting.value = true
  
  try {
    // Transform form data to match GraphQL schema
    const transformedData = transformFormData()
    
    // Emit the save event with transformed data
    emit('save', transformedData)
    
    // Reset form
    resetForm()
    
  } catch (error) {
    console.error('Error saving reserve:', error)
    errors.value.general = 'Failed to save reserve. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

// Reset form
const resetForm = () => {
  form.id = generateReserveId()
  form.name = ''
  form.type = ''
  form.label = ''
  form.description = ''
  form.bonuses = []
  form.deployables = []
  form.actions = []
  form.synergies = []
  errors.value = {}
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

.card {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  font-weight: 600;
}

.text-primary {
  color: #0d6efd !important;
}

.border-bottom {
  border-bottom: 2px solid #dee2e6 !important;
}
</style>