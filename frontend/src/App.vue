<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <SearchOperadoras />
  </div>
</template>

<script>
import SearchOperadoras from "./components/SearchOperadoras.vue";

export default {
  name: "App",
  components: {
    SearchOperadoras,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

img {
  width: 300px;
  height: 300px;
  margin-bottom: 20px;
}
</style>
