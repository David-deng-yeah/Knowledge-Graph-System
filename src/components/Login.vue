<template>
  <div class="my-login-wrap" id="my_login_wrap">
    <div id="my_brain"><img src="static/img_brain.png" style="width:80%;max-width:400px"/></div>
    <div class="my_title"><img src="static/logo.svg" width="30" valign="middle"/> &nbsp; 智慧纪检——智慧大脑<br/>
    </div>
    <div class="my-ms-login">
      <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content"
               v-loading="loginProgress" element-loading-text="Sending login request to server..."
               element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.8)">
        <el-form-item prop="user.name">
          <el-input
            tabindex=1
            v-model="param.user.name" placeholder="请输入用户名" :disabled="loginProgress">
            <el-button slot="prepend" icon="el-icon-user"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            tabindex=2
            type="password"
            placeholder="请输入密码"
            v-model="param.password"
            @keyup.enter.native="submitForm()"
            :disabled="loginProgress"
          >
            <el-button slot="prepend" icon="el-icon-lock"></el-button>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button
            tabindex=3
            type="primary" @click="submitForm()" :disabled="loginProgress">登录
          </el-button>
        </div>
        <!--TODO move to end of page-->
        <p class="login-tips" id="idTips"><a href="http://10.94.81.132/#/signin?disableAutoSignin=yes" target=_blank>Admin</a>
        </p>
      </el-form>
    </div>
    <div id="copyright">
      COPYRIGHT &copy; 深圳海关监察室<br/>
      POWERED BY 大数据系统计算国家工程实验室
    </div>
  </div>
</template>
<script>
  import bus from '../bus';
  import {get_menu_json_and_insert} from "../getMenu";

  export default {
    data: function () {
      return {
        param: {
          user: {name: ''}, password: '',
        },
        rules: {
          "user.name": [{required: true, message: '请输入用户名', trigger: 'blur'}],
          password: [{required: true, message: '请输入密码', trigger: 'blur'}],
        },
        loginProgress: false
      };
    },
    mounted() {
      try {
        draw_login_back(document.all('my_login_wrap'))// the element
      } catch (ex) {
      }
    },
    methods: {
      submitForm() {
        this.$refs.login.validate(valid => {
          if (valid) {
            let tips = this.jq(".login-wrap #idTips")
            tips.html("sending login request...")
            this.loginProgress = true
            let that = this
//wjc TODO change login bypass .py and use our ajax/rest...
            let request = this.jq.ajax({
              type: "get",
              url: "http://10.94.81.132:5000/login?username=" + this.param.user.name + "&password=" + this.param.password/*,
                        dataType:"jsonp",
                        jsonpCallback:"jsonp_cb"*/
            })
            request.done(function () {
              let ret = null
              //alert(request.responseText)
              eval("ret=" + request.responseText)
              if (ret.state == "succeeded") {
                that.$message.success('登录成功!');
                sessionStorage.setItem('tableau_backend_userid', ret.userid);
                sessionStorage.setItem('tableau_backend_username', ret.username);
                // sessionStorage.setItem('tableau_menu_a', '');
                bus.$emit('userinfo_changed', {id: ret.userid, name: that.param.user.name});

                setTimeout(get_menu_json_and_insert, 11);
                that.$router.push('/');
                tips.html("")
              } else if (ret.state == "failed") {
                that.$message.error('登录失败!');
                tips.html("<font color='red'>" + ret.error + "</font>")
              } else {
                tips.html("<font color='red'>unknown server response value!</font>")
              }
              that.loginProgress = false
            }).fail(function () {
              tips.html("<font color='red'>server error!</font>")
              that.loginProgress = false;
            })

          } else {
            this.$message.error('Please enter account name and credentials.');
            console.log('Submit failed!');
            return false;
          }
        });
      },
    },
  };
</script>

<style scoped>
  .my-login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    /*background-image: url(../assets/imgs/login-bg.jpg);*/
    /*
        background-color:#F4F4F4;
    */
    background-size: 100%;
  }

  #copyright {
    position: absolute;
    top: 90%;
    width: 100%;
    text-align: center;
    opacity: 0.5;
    font-size: 9pt;
  }

  #my_brain {
    position: absolute;
    left: 10%;
    top: 30%;
    width: 50%;
    height: 50%;
    opacity: 0.5;

    /*
        margin: -190px 0 0 -175px;
    */
    border-radius: 5px;
    /*
        background-repeat: no-repeat;
        background-image: url(/static/img_brain.png);
        background-position-y: center;
        background-size: 62%;
    */
    overflow: hidden;
  }

  .my-ms-login {
    position: absolute;
    left: 75%;
    top: 60%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    /*background: rgba(255, 255, 255, 0.3);*/
    background: white;
    overflow: hidden;
  }

  .login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    /*background-image: url(../assets/imgs/login-bg.jpg);*/
    background-size: 100%;
  }

  .my_title {
    position: absolute;
    left: 10%;
    top: 15%;
    padding-left: 0px;
    line-height: 50px;
    font-size: 24px;
    color: #409EFF;
  }

  .ms_title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: #409EFF;
    border-bottom: 1px solid #ddd;
  }

  .ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    /*background: rgba(255, 255, 255, 0.3);*/
    overflow: hidden;
  }

  .ms-content {
    padding: 30px 30px;
  }

  .login-btn {
    text-align: center;
  }

  .login-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
  }

  .login-tips {
    font-size: 12px;
    line-height: 30px;
    color: #fff;
    text-align: right;
  }
</style>
