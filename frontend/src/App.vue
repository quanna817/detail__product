<template>
  <Headers msg="Welcome to Your Vue.js App"/>
  <DetailProduct></DetailProduct>
</template>

<script>
import Headers from './components/Header.vue'
import DetailProduct from './components/DetailProduct.vue'
export default {
  name: 'App',
  components: {
    Headers,
    DetailProduct
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
