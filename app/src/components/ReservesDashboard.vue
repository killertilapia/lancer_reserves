<template>
  <div class="reserves-dashboard">
    <!-- Header Section -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <h1 class="h2 mb-0">
            <i class="bi bi-shield-check text-primary me-2"></i>
            Reserves Dashboard
          </h1>
          <button class="btn btn-primary" @click="openAddReserveModal">
            <i class="bi bi-plus-circle me-1"></i>
            Add Reserve
          </button>
        </div>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="row mb-4">
      <div class="col-12">
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          <i class="bi bi-exclamation-triangle me-2"></i>
          {{ error }}
          <button type="button" class="btn-close" @click="clearError" aria-label="Close"></button>
        </div>
      </div>
    </div>

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="row mb-4">
      <div class="col-12 text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading reserves...</p>
      </div>
    </div>

    <!-- Stats Cards -->
    <div v-if="!isLoading" class="row mb-4">
      <div class="col-md-3 mb-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title">Total Reserves</h6>
                <h3 class="mb-0">{{ totalReserves }}</h3>
              </div>
              <div class="align-self-center">
                <i class="bi bi-list-ul fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title">Bonus</h6>
                <h3 class="mb-0">{{ bonusReserves }}</h3>
              </div>
              <div class="align-self-center">
                <i class="bi bi-star fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title">Resource</h6>
                <h3 class="mb-0">{{ resourceReserves }}</h3>
              </div>
              <div class="align-self-center">
                <i class="bi bi-box fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 mb-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="card-title">Mech/Tactical</h6>
                <h3 class="mb-0">{{ mechReserves + tacticalReserves }}</h3>
              </div>
              <div class="align-self-center">
                <i class="bi bi-gear fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reserves Table -->
    <div v-if="!isLoading" class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="bi bi-table me-2"></i>
              Reserves
            </h5>
          </div>
            <div class="card-body">
              <div v-if="reserves.length === 0" class="text-center py-4">
                <i class="bi bi-inbox fs-1 text-muted"></i>
                <p class="text-muted mt-2">No reserves found. Create your first reserve!</p>
              </div>
              <div v-else class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Label</th>
                    <th>Type</th>                    
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="reserve in reserves" :key="reserve.id">
                    <td>
                      <code class="small">{{ reserve.id }}</code>
                    </td>
                    <td>
                      <strong>{{ reserve.name }}</strong>
                    </td>
                    <td>{{ reserve.label }}</td>
                    <td>{{  reserve.type }}</td>                    
                    <td>{{ formatDate(reserve.createdAt) }}</td>
                    <td>
                      <button 
                        class="btn btn-sm btn-outline-primary me-1"
                        @click="editReserve(reserve)"
                        title="Edit Reserve"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button 
                        class="btn btn-sm btn-outline-danger"
                        @click="confirmDeleteReserve(reserve)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Reserve Modal -->
    <AddReserveModal 
      v-if="showAddReserveModal"
      @close="closeAddReserveModal"
      @save="handleAddReserve"
    />

    <!-- Edit Reserve Modal -->
    <EditReserveModal 
      v-if="showEditReserveModal && selectedReserve"
      :reserve="selectedReserve"
      @close="closeEditReserveModal"
      @save="handleEditReserve"
    />

    <!-- Delete Confirm Modal -->
    <DeleteConfirmModal 
      v-if="showDeleteConfirmModal && selectedReserve"
      :reserve="selectedReserve"
      @close="closeDeleteConfirmModal"
      @confirm="handleDeleteReserve"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useReservesStore } from '../stores/reserves.js'
import { formatDate } from '../services/graphql.js'
import AddReserveModal from './AddReserveModal.vue'
import EditReserveModal from './EditReserveModal.vue'
import DeleteConfirmModal from './DeleteConfirmModal.vue'

// Use Pinia store
const reservesStore = useReservesStore()

// Use storeToRefs for reactive state
const {
  reserves,
  isLoading,
  error,
  showAddReserveModal,
  showEditReserveModal,
  showDeleteConfirmModal,
  selectedReserve,
  totalReserves,
  bonusReserves,
  resourceReserves,
  mechReserves,
  tacticalReserves,
  monthlyReserves
} = storeToRefs(reservesStore)

// Access actions directly from store
const {
  loadReserves,
  createReserve,
  updateReserve,
  deleteReserve,
  openAddReserveModal,
  closeAddReserveModal,
  openEditReserveModal,
  closeEditReserveModal,
  openDeleteConfirmModal,
  closeDeleteConfirmModal,
  clearError
} = reservesStore

// Methods
const editReserve = (reserve) => {
  openEditReserveModal(reserve)
}

const confirmDeleteReserve = (reserve) => {
  openDeleteConfirmModal(reserve)
}

const handleAddReserve = async (newReserve) => {
  try {
    await createReserve(newReserve)
  } catch (err) {
    // Error is handled in the store
    console.error('Failed to create reserve:', err)
  }
}

const handleEditReserve = async (id, updateData) => {
  try {
    await updateReserve(id, updateData)
  } catch (err) {
    // Error is handled in the store
    console.error('Failed to update reserve:', err)
  }
}

const handleDeleteReserve = async (id) => {
  try {
    await deleteReserve(id)
  } catch (err) {
    // Error is handled in the store
    console.error('Failed to delete reserve:', err)
  }
}

onMounted(() => {
  loadReserves()
})
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: box-shadow 0.15s ease-in-out;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.btn {
  border-radius: 0.375rem;
}
</style>
