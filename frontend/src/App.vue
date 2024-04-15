<template>
  <Headers msg="Welcome to Your Vue.js App"/>
  <DetailProduct></DetailProduct>
  <Chart></Chart>
</template>

<script>
import Headers from './components/Header.vue'
import DetailProduct from './components/DetailProduct.vue'
import Chart from './components/Chart.vue'
export default {
  name: 'App',
  components: {
    Headers,
    DetailProduct,
    Chart
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
  margin-top: 60px;
}
</style>
