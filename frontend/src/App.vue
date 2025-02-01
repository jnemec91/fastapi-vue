<template>
  <nav>
    <router-link :to="{name: 'home'}">Domů</router-link> | 
    <router-link :to="{name: 'about'}">O Aplikaci</router-link>
    <button v-if="!updatingDatabase" class=" top-right scraper-button" @click="startUpdate">Aktualizovat data</button>
    <div v-else class="top-right scraper-div">
      <p>Stahuji data...</p>
      <div class="loading small"></div>
      <p>Uloženo: {{ currentProgress }}</p>
      <p>Nalezeno piv: {{ totalProgress }}</p>
    </div>

  </nav>
  <div class="page">
    <router-view/>
  </div>
</template>

<script>
 // using options API
export default {
  data() {
    return {
      error: '',
      updatingDatabase: false,
      currentProgress: 0,
      totalProgress: 0
    }
  },
  methods: {
    async checkStatus(task_id) {
      const statusResponse = await fetch(`http://127.0.0.1:8000/beers/tasks/${task_id}`)
      const statusData = await statusResponse.json()
      if (statusData.status === 'SUCCESS') {
        this.currentProgress = 0
        this.totalProgress = 0        
        this.updatingDatabase = false
        
      } else if (statusData.status === 'FAILURE') {
        this.currentProgress = 0
        this.totalProgress = 0
        this.updatingDatabase = false
        alert('Error updating database!')

      } else if (statusData.status === 'PROGRESS') {
        this.currentProgress = statusData.progress.current
        this.totalProgress = statusData.progress.total
        setTimeout(() => this.checkStatus(task_id), 1000)
      } else {
        setTimeout(() => this.checkStatus(task_id), 1000)
      }
    },
    async startUpdate() {
      this.updatingDatabase = true
      try {
        let response = await fetch('http://127.0.0.1:8000/beers/scrape')
        if (!response.ok) {
          throw Error('Unable to update database now!')
        }
        const data = await response.json()
        
        this.checkStatus(data.task_id)
      }
      catch (err) {
        this.error = err.message
        alert(this.error)
        this.updatingDatabase = false
      }
    }
  },
  mounted() {
    fetch('http://127.0.0.1:8000/tasks/running')
    .then(response => response.json())
    .then(data => {
      if (data.tasks.length > 0) {
        this.updatingDatabase = true
        this.checkStatus(data.tasks[0])
      }
    })
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

.scraper-div{
  border: 4px solid crimson;
  border-radius: 12px;
  background: white;
  padding: 5px;
  font-weight: bold;
}
.scraper-div > .loading{
  margin: 0 auto;
}

.scraper-button{
  border: 2px solid transparent;
  border-radius: 4px;
  background: crimson;
  color: whitesmoke;
  padding: 10px;
  font-size: 16px;
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

.small{
  width: 10px;
  height: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
