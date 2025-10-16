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
          <button class="btn btn-primary" @click="showAddReserveModal = true">
            <i class="bi bi-plus-circle me-1"></i>
            Add Reserve
          </button>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
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
                <h6 class="card-title">Active</h6>
                <h3 class="mb-0">{{ activeReserves }}</h3>
              </div>
              <div class="align-self-center">
                <i class="bi bi-check-circle fs-1"></i>
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
                <h6 class="card-title">Pending</h6>
                <h3 class="mb-0">{{ pendingReserves }}</h3>
              </div>
              <div class="align-self-center">
                <i class="bi bi-clock fs-1"></i>
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
                <h6 class="card-title">This Month</h6>
                <h3 class="mb-0">{{ monthlyReserves }}</h3>
              </div>
              <div class="align-self-center">
                <i class="bi bi-calendar-month fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reserves Table -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="bi bi-table me-2"></i>
              Recent Reserves
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="reserve in reserves" :key="reserve.id">
                    <td>{{ reserve.id }}</td>
                    <td>{{ reserve.name }}</td>
                    <td>
                      <span class="badge bg-secondary">{{ reserve.type }}</span>
                    </td>
                    <td>
                      <span 
                        class="badge" 
                        :class="{
                          'bg-success': reserve.status === 'active',
                          'bg-warning': reserve.status === 'pending',
                          'bg-danger': reserve.status === 'inactive'
                        }"
                      >
                        {{ reserve.status }}
                      </span>
                    </td>
                    <td>{{ formatDate(reserve.createdAt) }}</td>
                    <td>
                      <button 
                        class="btn btn-sm btn-outline-primary me-1"
                        @click="editReserve(reserve)"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button 
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteReserve(reserve.id)"
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
      @close="showAddReserveModal = false"
      @save="handleAddReserve"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AddReserveModal from './AddReserveModal.vue'

// Reactive data
const reserves = ref([
  {
    id: 1,
    name: 'Emergency Fund',
    type: 'Financial',
    status: 'active',
    createdAt: new Date('2024-01-15')
  },
  {
    id: 2,
    name: 'Equipment Reserve',
    type: 'Physical',
    status: 'pending',
    createdAt: new Date('2024-01-20')
  },
  {
    id: 3,
    name: 'Personnel Backup',
    type: 'Human',
    status: 'active',
    createdAt: new Date('2024-01-25')
  }
])

const showAddReserveModal = ref(false)

// Computed properties
const totalReserves = computed(() => reserves.value.length)
const activeReserves = computed(() => reserves.value.filter(r => r.status === 'active').length)
const pendingReserves = computed(() => reserves.value.filter(r => r.status === 'pending').length)
const monthlyReserves = computed(() => {
  const currentMonth = new Date().getMonth()
  const currentYear = new Date().getFullYear()
  return reserves.value.filter(r => {
    const reserveDate = new Date(r.createdAt)
    return reserveDate.getMonth() === currentMonth && reserveDate.getFullYear() === currentYear
  }).length
})

// Methods
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const editReserve = (reserve) => {
  console.log('Edit reserve:', reserve)
  // TODO: Implement edit functionality
}

const deleteReserve = (id) => {
  if (confirm('Are you sure you want to delete this reserve?')) {
    reserves.value = reserves.value.filter(r => r.id !== id)
  }
}

const handleAddReserve = (newReserve) => {
  const id = Math.max(...reserves.value.map(r => r.id)) + 1
  reserves.value.push({
    id,
    ...newReserve,
    createdAt: new Date()
  })
  showAddReserveModal.value = false
}

onMounted(() => {
  console.log('ReservesDashboard mounted')
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
