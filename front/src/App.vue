<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <CountryTable msg="sadasdasdasds App"/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import CountryTable from './components/CountryTable.vue'

// console.log(HelloWorld);
// console.log(CountryTable);

export default {
  name: 'App',
  components: {
    HelloWorld,
    CountryTable
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
