<template>
  <div>
    <template v-for="item in items">
      <template v-if="item.subs">
        <el-submenu :index="item.index" :key="item.index">
          <template slot="title">
            <i :class="item.icon"></i>
            <span slot="title">{{ item.title }}</span>
          </template>
          <template v-for="subItem in item.subs">
            <el-submenu
              v-if="subItem.subs"
              :index="subItem.index"
              :key="subItem.index"
            >
              <template slot="title">{{ subItem.title }}</template>
            </el-submenu>
            <el-menu-item
              v-else
              :index="subItem.index"
              :key="subItem.index"
            >{{ subItem.title }}
            </el-menu-item>
          </template>
        </el-submenu>
      </template>
      <template v-else>
        <el-menu-item :index="item.index" :key="item.index">
          <i :class="item.icon"></i>
          <span slot="title">{{ item.title }}</span>
        </el-menu-item>
      </template>
    </template>
  </div>
</template>

<script>

  export default {
    name: 'Sidebar_dev',
    data() {
      return {
        items: [
          {
            icon: 'el-icon-user-solid',
            index: 'admin',
            title: '管理员权限',
            subs: [
              {
                index: 'ConfigRouters',
                title: '配置路由'
              },
              {
                index: 'ConfigHybrid',
                title: '配置混编页面'
              },
              {
                index: 'Message',
                title: '定时获取信息'
              }
            ]
          },
        ]
      };
    }
  };
</script>

<style scoped>
  .el-menu--collapse .el-submenu__title span {
    display: none;
  }

  .el-menu--collapse .el-submenu__title .el-submenu__icon-arrow {
    display: none;
  }
</style>
