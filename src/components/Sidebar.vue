<template>
  <div class="sidebar">
    <el-menu
      class="sidebar-el-menu"
      :collapse="collapse"
      background-color="#324157"
      text-color="#bfcbd9"
      active-text-color="#20a0ff"
      :default-openeds="['prod']"
      router
    >
      <template v-for="(item, i) in items">
        <template v-if="item.subs">
          <el-submenu :index="item.index" :key="i">
            <template slot="title">
              <i :class="item.icon"></i>
              <span slot="title">{{ item.title }}</span>
            </template>
            <template v-for="(subItem, i) in item.subs">
              <el-submenu
                v-if="subItem.subs"
                :index="subItem.index"
                :key="i"
              >
                <template slot="title">{{ subItem.title }}</template>
                <el-menu-item
                  v-for="(threeItem, i) in subItem.subs"
                  :key="i"
                  :index="threeItem.index">
                  {{threeItem.title}}
                </el-menu-item>
              </el-submenu>
              <el-menu-item
                v-else
                :index="subItem.index"
                :key="i"
              >{{ subItem.title }}
              </el-menu-item>
            </template>
          </el-submenu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index" :key="i">
            <i :class="item.icon"></i>
            <span slot="title">{{ item.title }}</span>
          </el-menu-item>
        </template>
      </template>
      <vSidebarDev v-show="show_dev"></vSidebarDev>
    </el-menu>
  </div>
</template>

<script>
  import bus from '../bus';
  import vSidebarDev from './SidebarDev'

  let gData = {
    show_dev: false,
    collapse: false,
    // items: [],//TODO replace later by
    items: [
      {
        icon: 'el-icon-menu',
        index: 'prod',
        title: '主要功能',
        subs: [
          {
            index: 'tableau',
            title: '智慧大脑'
          },
          {
            index: 'bgd',
            title: '报关单查询'
          },
          {
            index: 'bgd_atlas',
            title: '报关单图谱'
          },
        ]
      }
    ]
  };
  let flag = false;
  function init_menu() {
    // i_counter++; if (i_counter>max) { alert('too long');... }
    let username = sessionStorage.getItem('tableau_backend_username');
    if (username == 'kjr' || username == 'test') gData.show_dev = true;
    //TODO
    // let m_a = await (await fetch('../static/router.json')).json(); //TODO replace remote api from :5000
    let menu_a_s = sessionStorage.getItem('tableau_menu_a');
    // console.log('menu_a_s=',menu_a_s);
    let m_a = s2o(menu_a_s || '');
    if (m_a) {
      //flag
      if (!flag){
        for (let m in m_a.router) {
          let _item;
          let v = m_a.router[m] || {};
          if (v.children) {
            let subs = [];
            for (let c in v.children) {
              subs.push({
                index: v.children[c].path,
                title: v.children[c].meta.title
              })
            }
            _item = {
              index: v.path,
              title: v.meta.title,
              subs: subs,
            }
          } else {
            _item = {
              index: v.path,
              title: v.meta.title,
            };
          }
          gData.items[0].subs.push(_item);
        }
        flag = true;
      } else {
        return;
      }
      //TODO json (from db): [ {lvl:1, title, url}, {lvl:2}  ], or [ {id, lvl, title, url, pid}, ... ]
    } else {
      console.log(111)
      setTimeout(init_menu, 1111);
    }
  }
  export default {
    name: 'Sidebar',
    components: {vSidebarDev},
    data() {
      return gData;
    },
    inject: ['reload'],
    async mounted() {
      init_menu();
    },
    computed: {
      routes() {
        // alert('TODO routes()')
        return this.$route.path.replace('/', '');
      }
    },
    created() {
      //alert('TODO created')
      // 通过 Event Bus 进行组件间通信，来折叠侧边栏
      bus.$on('collapse', msg => {
        this.collapse = msg;
        bus.$emit('collapse-content', msg);
      });
    }
  };
</script>

<style scoped>
  .sidebar {
    display: block;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    overflow-y: scroll;
  }

  .sidebar::-webkit-scrollbar {
    width: 0;
  }

  .sidebar-el-menu:not(.el-menu--collapse) {
    width: 250px;
  }

  .sidebar > ul {
    height: 100%;
  }
</style>
