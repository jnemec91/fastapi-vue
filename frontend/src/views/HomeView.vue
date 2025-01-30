<template>
  <div class="home">
    <h1>Interaktivní seznam piva</h1>
  </div>
  <BeerTable/>
</template>

<script>
// @ is an alias to /src
import BeerTable from "@/components/BeerTable.vue";

export default {
  name: 'HomeView',
  data () {
    return {

    }
  },
  components: {
    BeerTable
  }
}
</script>

<style>

</style>