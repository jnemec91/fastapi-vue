import { ref } from "vue";

const getBeerData = () => {
    const beers = ref([])
    const error = ref(null)

    const load = async (url) => {
        try {
          let data = await fetch(url)
          if (!data.ok) {
            throw Error('No data available')
          }
          beers.value = await data.json()
          return data
        }
        catch (err){
          error.value = err.message
          alert(error.value)
        }
      }
      return { beers, error, load }
}

export default getBeerData