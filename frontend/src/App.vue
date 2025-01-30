<template>
  <nav>
    <router-link :to="{name: 'home'}">Domů</router-link> | 
    <router-link :to="{name: 'about'}">O Aplikaci</router-link>
    <button v-if="!updatingDatabase" class=" top-right scraper-button" @click="startUpdate">Aktualizovat data</button>
    <div v-else class="top-right loading">

    </div>
  </nav>
  <div class="page">
    <router-view/>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const error = ref('')
    const updatingDatabase = ref(false)
    
    const startUpdate = async () => {
      updatingDatabase.value = true
      try {
        let response = await fetch('http://127.0.0.1:8000/beers/scrape')
        if (!response.ok) {
          throw Error('Unable to update database now!')
        }
        const data = await response.json()
        
        // Poll for task completion
        const checkStatus = async () => {
          const statusResponse = await fetch(`http://127.0.0.1:8000/beers/scrape/${data.task_id}`)
          const statusData = await statusResponse.json()
          if (statusData.status === 'SUCCESS') {
            updatingDatabase.value = false
          } else if (statusData.status === 'FAILURE') {
            throw Error('Task failed')
          } else {
            setTimeout(checkStatus, 1000) // Check again in 1 second
          }
        }
        
        checkStatus()
      }
      catch (err) {
        error.value = err.message
        alert(error.value)
        updatingDatabase.value = false
      }
    }
    return {
      startUpdate, error, updatingDatabase
    }
  }
}



</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  padding: 10px;
  border: 2px solid transparent;
  border-radius: 4px;
}

nav a.router-link-exact-active {
  background-color: #f28e1c;
  color: whitesmoke;
}

.top-right{
  z-index: 2;
  position: fixed;
  top: 20px;
  right: 20px;  
}

.scraper-button{
  border: none;
  border-radius: 4px;
  background: crimson;
  color: whitesmoke;
  padding: 10px;
  font-size: 20px;
  cursor: pointer;
  font-weight: bold;
}

.scraper-button:hover{
  border: 2px solid crimson;
  background-color: white;
  color: crimson;
}

nav{
  position: fixed;
  top: 0;
  left: 0;
  height: 2vh;
  width: 100vw;
  background-color: white;
  border-bottom: 4px solid #f28e1c;
  margin: 0;
  z-index: 1;
}
.page{
  margin: 12vh 0 0 0;
}
.loading {
  top: 10px;
  border: 16px solid #f3f3f3; /* Light grey */
  border-top: 16px solid crimson; /* Blue */
  border-radius: 50%;
  width: 25px;
  height: 25px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
