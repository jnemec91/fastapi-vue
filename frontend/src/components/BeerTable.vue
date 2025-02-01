<template>
    <div>
        <label class="search-label">Hledat: </label>
        <input type="text" placeholder="Hledaná fráze" v-model="searchBeer">
        <div>
            <label class="radio-label">Jméno</label>
            <input name='search-filter' type="radio" value="name" v-model="searchFilter">
            <label class="radio-label">Styl</label>
            <input name='search-filter' type="radio" value="style" v-model="searchFilter">
            <label class="radio-label">ABV</label>
            <input name='search-filter' type="radio" value="abv" v-model="searchFilter">
            <label class="radio-label">EPM</label>
            <input name='search-filter' type="radio" value="ibu" v-model="searchFilter">
            <label class="radio-label">Pivovar</label>
            <input name='search-filter' type="radio" value="brewery" v-model="searchFilter">
            <label class="radio-label">Rating</label>
            <input name='search-filter' type="radio" value="rating" v-model="searchFilter">
        </div>
    </div>
    <table>
      <thead>
        <tr class="table-header">
            <th>
                <button @click="sortData('name')"  v-bind:class="{'selected' : sortKey ==='name' }">
                    Jméno 
                    <span v-if="sortDirection==='desc' && sortKey ==='name'" class="sort-indicator">↓</span>
                    <span v-else-if="sortDirection==='asc' && sortKey ==='name'" class="sort-indicator">↑</span>
                </button>
            </th>
            <th>
                <button @click="sortData('style')"  v-bind:class="{'selected' : sortKey ==='style' }">
                    Styl
                    <span v-if="sortDirection==='desc' && sortKey ==='style'" class="sort-indicator">↓</span>
                    <span v-else-if="sortDirection==='asc' && sortKey ==='style'" class="sort-indicator">↑</span>                
                </button>
            </th>
            <th>
                <button @click="sortData('abv')"  v-bind:class="{'selected' : sortKey ==='abv' }">
                    ABV
                    <span v-if="sortDirection==='desc' && sortKey ==='abv'" class="sort-indicator">↓</span>
                    <span v-else-if="sortDirection==='asc' && sortKey ==='abv'" class="sort-indicator">↑</span>  
                </button>
            </th>
            <th>
                <button @click="sortData('epm')" v-bind:class="{'selected' : sortKey ==='epm' }">
                    EPM
                    <span v-if="sortDirection==='desc' && sortKey ==='epm'" class="sort-indicator">↓</span>
                    <span v-else-if="sortDirection==='asc' && sortKey ==='epm'" class="sort-indicator">↑</span>  
                </button>
            </th>
            <th>
                <button @click="sortData('brewery')" v-bind:class="{'selected' : sortKey ==='brewery' }">
                    Pivovar
                    <span v-if="sortDirection==='desc' && sortKey ==='brewery'" class="sort-indicator">↓</span>
                    <span v-else-if="sortDirection==='asc' && sortKey ==='brewery'" class="sort-indicator">↑</span>  
                </button>
            </th>
            <th>
                <button @click="sortData('rating')" v-bind:class="{'selected' : sortKey ==='rating' }">
                    Rating
                    <span v-if="sortDirection==='desc' && sortKey ==='rating'" class="sort-indicator">↓</span>
                    <span v-else-if="sortDirection==='asc' && sortKey ==='rating'" class="sort-indicator">↑</span>  
                </button>
            </th>
        </tr>
      </thead>
      <tbody v-if="beers.length > 0">
        <tr v-for="beer in filteredData" :key="beer.id" @click="selectedBeer = beer">
          <td>{{ beer.name }}</td>
          <td>{{ beer.style }}</td>
          <td>{{ beer.abv }}</td>
          <td>{{ beer.epm }}</td>
          <td>{{ beer.brewery }}</td>
          <td>{{ beer.rating }}</td>
        </tr>
      </tbody>
      <div v-else class="center">
        <div class="loading orange"></div>
        <h2 class="loading-text">Loading...</h2>
      </div>
  </table>
  <div v-if="selectedBeer!=null">
    <beerModal :beer="selectedBeer" @closeBeerModal="selectedBeer = null"/>
  </div>
  
</template>

<script>
// using composition API
import getBeerData from "@/composables/getBeerData.js"
import beerModal from '@/components/BeerModal.vue'
import { ref, computed } from 'vue'

export default {
  name: 'BeerTable',
  components: {
    beerModal
  },
  setup() {
    const selectedBeer = ref(null)
    const searchBeer = ref('')
    const searchFilter = ref('name')
    const { beers, error, load } = getBeerData()

    const sortKey = ref('name')
    const sortDirection = ref('asc')
    
    load('http://127.0.0.1:8000/beers')

    const filteredData = computed(() => {
    return beers.value.filter((beer) => {
        
        const propertyValue = beer[searchFilter.value]?.toString().toLowerCase() ?? ''
        const searchValue = searchBeer.value.toLowerCase()
        
        if (typeof propertyValue === 'number') {
            return propertyValue.toString().includes(searchValue)
        }
        return propertyValue.includes(searchValue)
    })
})

    const sortData = (key) => {
        sortKey.value = key
        if(sortDirection.value === 'asc'){
            sortDirection.value = 'desc'
            beers.value.sort((a, b) => a[sortKey.value] > b[sortKey.value] ? 1 : -1)
        } else {
            sortDirection.value = 'asc'
            beers.value.sort((a, b) => a[sortKey.value] < b[sortKey.value] ? 1 : -1)
        }
    }
    console.log(selectedBeer.value)
    return {
        beers, error, searchBeer, filteredData, sortData, sortDirection, sortKey, searchFilter, selectedBeer
    }
  },
}
</script>

<style>
    table{
    width: 90vw;
    margin: 20px 5vw;
    }
    th, td{ 
    width: 15vw;
    border: none;
    margin: 0;
    }
    th > button{
    border: 2px solid transparent;
    border-radius: 4px;
    background: #f28e1c;
    color: whitesmoke;
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
    font-weight: bold;
    }
    th > button:hover{
        background: white;
        border: 2px solid #f28e1c;
        color: #f28e1c;
    }
    th > button.selected{
        background: white;
        border: 2px solid #f28e1c;
        color: #f28e1c;
    }
    tr{
        position: relative;
    }
    tr:hover{
        background: #ddd;
        cursor: pointer;
    }
    tr::after{
        content: "";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        width: 90vw;
        border:1px solid #444 ;
    }
    tr.table-header:hover{
        background: white;
        cursor: default;
    }
    tr.table-header::after{
        display: none;
    }
    td{
        padding: 10px 0;
    }
    .search-label{
        font-weight: bolder;
        font-size: larger;
    }
    input[type='text']{
        width: 33vw;
        height: 30px;
        border-radius: 10px;
    }
    input[type='radio']{
        margin: 10px 30px 20px 4px;
    }    
    .sort-indicator {
        margin-left: 4px;
        font-weight: bold;
    }
    .radio-label{
        font-weight: bold;
    }
    .orange{
        border-top: 16px solid #f28e1c;
    }
    .loading-text{
        font-size: 24px;
        font-weight: bold;
        transform: translateX(-20px);
    }
    .center{
        position: absolute;
        top: 50%;
        left: 50%;
        text-align: center;
    }
</style>