<template>
  <div id="app">
    <router-view v-if="isRouterAlive"></router-view>
  </div>
</template>
<script>
  import vHome from './components/Home.vue';

  export default {
    name: 'app',
    components: {
      vHome
    },
    provide() {
      return {
        reload: this.reload
      }
    },
    data() {
      return {
        isRouterAlive: true
      }
    },
    methods: {
      reload() {
        this.isRouterAlive = false;
        this.$nextTick(function () {
          this.isRouterAlive = true
        });
      }
    }
  }
</script>
<style>
  /*@import "./assets/css/theme-green/color-green.css";*/
</style>
