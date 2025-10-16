<template>
  <div id="app">
    <NavBar />
    <main class="container-fluid py-4">
      <router-view v-if="false" />
      <ReservesDashboard v-else />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from './components/NavBar.vue'
import ReservesDashboard from './components/ReservesDashboard.vue'

// App state
const isLoading = ref(false)

onMounted(() => {
  console.log('Lancer Reserves App mounted')
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
