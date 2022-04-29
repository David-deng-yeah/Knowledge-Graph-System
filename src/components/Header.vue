<template>
  <div class="header">
    <!-- a rectangle shape to collapse the left vertical menu -->
    <div class="collapse-btn" @click="collapseChanged">
      <i><img src="static/logo.svg" alt="china custom logo" width="30" valign="middle"></i>
    </div>
    <div class="logo">智慧纪检</div>
    <div class="header-right">
      <div class="header-user-con">
        <!-- fullscreen button -->
        <div class="btn-fullscreen" @click="handleFullScreen">
          <el-tooltip effect="dark" :content="fullscreen?`exit fullscreen`:`enter fullscreen`" placement="bottom">
            <i class="el-icon-rank"></i>
          </el-tooltip>
        </div>
        <!-- 'message center' icon -->
        <div class="btn-bell">
          <el-tooltip
            effect="dark"
            :content="message?`There are ${message} unread messages.`:`Show the message center.`"
            placement="bottom"
          >
            <router-link to="/tabs">
              <i class="el-icon-bell"></i>
            </router-link>
          </el-tooltip>
          <span class="btn-bell-badge" v-if="message"></span>
        </div>
        <!-- user icon -->
        <div class="user-avator">
          <img src="../assets/imgs/user_img.jpg"/>
        </div>
        <!-- user dropdown menu -->
        <el-dropdown class="user-name" trigger="click" @command="handleUserMenuCommand">
                    <span class="el-dropdown-link">
                        {{username}}
                        <i class="el-icon-caret-bottom"></i>
                    </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item divided command="config">用户信息</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>
<script>
  import bus from '../bus';

  export default {
    data() {
      return {
        collapse: false,
        fullscreen: false,
        name: 'username',
        message: 2,
        userid: null
      };
    },
    computed: {
      username() {
        let username = sessionStorage.getItem('tableau_backend_username');
        return username ? username : this.name;
      }
    },
    methods: {
      // left vertical menu 'horizontal collapse' button
      collapseChanged() {
        this.collapse = !this.collapse;
        bus.$emit('collapse', this.collapse);
      },
      // fullscreen button
      handleFullScreen() {
        let element = document.documentElement;
        if (this.fullscreen) {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
          }
        } else {
          if (element.requestFullscreen) {
            element.requestFullscreen();
          } else if (element.webkitRequestFullScreen) {
            element.webkitRequestFullScreen();
          } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
          } else if (element.msRequestFullscreen) {
            // IE11
            element.msRequestFullscreen();
          }
        }
        this.fullscreen = !this.fullscreen;
      },
      // user dropdown menu button
      handleUserMenuCommand(command) {
        if (command == 'logout') {
          let logout_note = this.$notify({
            title: 'Logout',
            message: 'Sending logout request...',
            duration: 0,
            position: 'bottom-right'
          });
          let that = this
          let request = this.jq.ajax({
            type: "get",
            url: "http://10.94.81.132:5000/logout?userid=" + this.userid,
          })
          request.done(function () {
            let ret = null
            eval("ret=" + request.responseText)
            if (ret.state == "succeeded") {
              that.$message.success('Logout successful!');
              //notes: no need to clear the common tableau menu data:
              // sessionStorage.setItem('tableau_menu_a', '');
            } else if (ret.state == "failed") {
              that.$message.error('Logout failed: ' + ret.error);
            } else {
              that.$message.error("<font color='red'>Logout failed: unknown server response value!</font>")
            }
            logout_note.close()
            that.$router.push('/login');
          }).fail(function () {
            that.$message.error("<font color='red'>Logout failed: server error!</font>")
            logout_note.close()
            that.$router.push('/login');
          })

          sessionStorage.removeItem('tableau_backend_userid');
          sessionStorage.removeItem('tableau_menu_a');
          sessionStorage.removeItem('tableau_backend_username');
          this.userid = null
          bus.$emit('userinfo_changed', null);
        }
      }
    },
    mounted() {
      if (document.body.clientWidth < 1500) {
        this.collapseChanged();
      }

      let userid = sessionStorage.getItem('tableau_backend_userid');
      if (userid == null) {
        this.$message.warning('Login required!');
        this.$router.push('/login');
      } else {
        this.userid = userid;
      }
    }
  };
</script>
<style scoped>
  .header {
    position: relative;
    box-sizing: border-box;
    width: 100%;
    height: 70px;
    font-size: 22px;
    color: #fff;
  }

  .collapse-btn {
    float: left;
    padding: 0 21px;
    cursor: pointer;
    line-height: 70px;
  }

  .header .logo {
    float: left;
    width: 250px;
    line-height: 70px;
  }

  .header-right {
    float: right;
    padding-right: 50px;
  }

  .header-user-con {
    display: flex;
    height: 70px;
    align-items: center;
  }

  .btn-fullscreen {
    transform: rotate(45deg);
    margin-right: 5px;
    font-size: 24px;
  }

  .btn-bell {
    display: none; /* TODO tmp hide bell */
    position: relative;
    width: 30px;
    height: 30px;
    text-align: center;
    border-radius: 15px;
    cursor: pointer;
  }

  .btn-fullscreen {
    position: relative;
    width: 30px;
    height: 30px;
    text-align: center;
    border-radius: 15px;
    cursor: pointer;
  }

  .btn-bell-badge {
    position: absolute;
    right: 0;
    top: -2px;
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background: #f56c6c;
    color: #fff;
  }

  .btn-bell .el-icon-bell {
    color: #fff;
  }

  .user-name {
    margin-left: 10px;
  }

  .user-avator {
    margin-left: 20px;
    display: none; /* TODO no need now */
  }

  .user-avator img {
    display: block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }

  .el-dropdown-link {
    color: #fff;
    cursor: pointer;
  }

  .el-dropdown-menu__item {
    text-align: center;
  }
</style>
