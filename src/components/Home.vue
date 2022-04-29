<template>
  <!--<img src="./assets/logo.png">-->
  <div class="wrapper">
    <!-- area above others: -->
    <v-head></v-head>

    <!-- left vertical menu: -->
    <v-sidebar></v-sidebar>

    <!-- contents beside menu: -->
    <div class="content-box" :class="{'content-collapse':collapse}">
      <!-- some toolbar buttons: -->
      <v-toolbar></v-toolbar>

      <!-- tab or other panels: -->
      <div class="content" id=idContentArea>
        <transition name="move" mode="out-in">
          <keep-alive :include="viewsList">
            <router-view></router-view>
          </keep-alive>
        </transition>

        <!-- 'return to top' button: -->
        <el-backtop target=".content"></el-backtop>
      </div>
    </div>
  </div>
</template>

<script>
  import vHead from './Header.vue';
  import vSidebar from './Sidebar.vue';
  import vToolbar from './Tags.vue';
  import bus from '../bus';

  export default {
    //this name is usually used for recursive appearance of a component.
    name: 'home',
    //By convention the data members of a component must be wrapped in a function.
    data() {
      return {
        //used by router-view and keep-alive
        _viewsNames: {},
        viewsList: [],

        //control the visibility of left vertical menu
        collapse: false,

        //login information
        username: 'empty user name',
        userid: null
      };
    },
    //This is a shortcut for vHead: vHead, etc.
    //These will allow v-head and other tags being used in this component only.
    components: {
      vHead,
      vSidebar,
      vToolbar
    },
    //called before the dom element is created
    created() {
      bus.$on('collapse-content', msg => {
        this.collapse = msg;
      });

      // keep-alive can cache router pages, the following allows for caching opened tabs.
      bus.$on('add-views', msg => {
        for (let i = 0, len = msg.length; i < len; i++) {
          var name = msg[i]
          if (!name in this._viewsNames) {
            this.viewsList.push(name);
            this._viewsNames[name] = true;
          }
        }
      });
      bus.$on('del-views', msg => {
        for (let i = 0, len = msg.length; i < len; i++) {
          var name = msg[i]
          if (name in this._viewsNames) {
            delete this._viewsNames[name];
          }
        }
        viewsList = []
        for (key in this._viewsNames) {
          this.viewsList.push(key)
        }
      });

      bus.$on('userinfo_changed', new_value => {
        this.userid = new_value.id;
        this.username = new_value.name
      });

      for (key in this._viewsNames) {
        this.viewsList.push(key)
      }
    },
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;

  }

  /* When left vertical menu is invisible, show some space. */
  .content-collapse {
    left: 65px;
  }

</style>
