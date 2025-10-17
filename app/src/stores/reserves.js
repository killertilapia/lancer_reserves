import { defineStore } from 'pinia'
import { api, RESERVE_TYPES } from '../services/graphql.js'

export const useReservesStore = defineStore('reserves', {
  state: () => ({
    reserves: [],
    isLoading: false,
    error: null,
    showAddReserveModal: false,
    showEditReserveModal: false,
    showDeleteConfirmModal: false,
    selectedReserve: null
  }),

  getters: {
    totalReserves: (state) => state.reserves.length,
    
    bonusReserves: (state) => state.reserves.filter(r => r.type === RESERVE_TYPES.BONUS).length,
    
    resourceReserves: (state) => state.reserves.filter(r => r.type === RESERVE_TYPES.RESOURCE).length,
    
    mechReserves: (state) => state.reserves.filter(r => r.type === RESERVE_TYPES.MECH).length,
    
    tacticalReserves: (state) => state.reserves.filter(r => r.type === RESERVE_TYPES.TACTICAL).length,

    monthlyReserves: (state) => {
      const currentMonth = new Date().getMonth()
      const currentYear = new Date().getFullYear()
      return state.reserves.filter(r => {
        const reserveDate = new Date(r.createdAt)
        return reserveDate.getMonth() === currentMonth && reserveDate.getFullYear() === currentYear
      }).length
    }
  },

  actions: {
    async loadReserves() {
      this.isLoading = true
      this.error = null
      
      try {
        this.reserves = await api.fetchReserves()
      } catch (err) {
        this.error = `Failed to load reserves: ${err.message}`
        console.error('Error loading reserves:', err)
      } finally {
        this.isLoading = false
      }
    },

    async createReserve(reserveData) {
      try {
        const newReserve = await api.createReserve(reserveData)
        this.reserves.push(newReserve)
        this.showAddReserveModal = false
        return newReserve
      } catch (err) {
        this.error = `Failed to create reserve: ${err.message}`
        console.error('Error creating reserve:', err)
        throw err
      }
    },

    async updateReserve(id, updateData) {
      try {
        const updatedReserve = await api.updateReserve(id, updateData)
        const index = this.reserves.findIndex(r => r.id === id)
        if (index !== -1) {
          this.reserves[index] = updatedReserve
        }
        this.showEditReserveModal = false
        this.selectedReserve = null
        return updatedReserve
      } catch (err) {
        this.error = `Failed to update reserve: ${err.message}`
        console.error('Error updating reserve:', err)
        throw err
      }
    },

    async deleteReserve(id) {
      try {
        await api.deleteReserve(id)
        this.reserves = this.reserves.filter(r => r.id !== id)
        this.showDeleteConfirmModal = false
        this.selectedReserve = null
      } catch (err) {
        this.error = `Failed to delete reserve: ${err.message}`
        console.error('Error deleting reserve:', err)
        throw err
      }
    },

    // Modal management actions
    openAddReserveModal() {
      this.showAddReserveModal = true
    },

    closeAddReserveModal() {
      this.showAddReserveModal = false
    },

    openEditReserveModal(reserve) {
      this.selectedReserve = reserve
      this.showEditReserveModal = true
    },

    closeEditReserveModal() {
      this.showEditReserveModal = false
      this.selectedReserve = null
    },

    openDeleteConfirmModal(reserve) {
      this.selectedReserve = reserve
      this.showDeleteConfirmModal = true
    },

    closeDeleteConfirmModal() {
      this.showDeleteConfirmModal = false
      this.selectedReserve = null
    },

    clearError() {
      this.error = null
    }
  }
})
