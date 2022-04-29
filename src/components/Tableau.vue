<template>
  <div class='tableau-view'>
    <!--
    <el-button type="info" icon="el-icon-refresh" @click="handleRefresh()" size=mini>refresh</el-button>
    <span class="breadcrumbs" id="view_levels">
      <span><a href="javascript:1" @click="handleHome()"><i class="el-icon-s-home" style="margin-right:10px"></i>Projects</a><span class=sep>/</span></span>
      <span><a href="javascript:show_iframe()">last level</a><span class=sep>/</span></span>
    </span>
    -->
    <el-row :gutter="0" justify="end" style="padding-top:0" id="idContentTableauHeader">
      <el-col :span="20">
        <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-left:5px">
          <el-breadcrumb-item :to="{ path: '/tableau' }">
            <i class="el-icon-s-home" style="margin-right:10px"></i>Projects
          </el-breadcrumb-item>
          <el-breadcrumb-item v-for="item in nav_items" :to="{ path: item.path }">{{item.title}}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-col>
      <el-col :span="4" style="text-align:right">
        <el-button type="info" icon="el-icon-refresh" @click="handleRefresh()" size=mini style="margin-right:5px">
          refresh
        </el-button>
      </el-col>
    </el-row>
    <div class="main-content"
         v-loading="loading"
         :element-loading-text="loadingMsg"
         element-loading-spinner="el-icon-loading"
         element-loading-background="rgba(0, 0, 0, 0.8)">
      <div class="container" id=contentList>
        <v-tableau-list-item v-for="item of listdata"
                           :itemdata="item"
                           :baseurl="baseurl"
                           @menu="handleShowMenu">
        </v-tableau-list-item>
      </div>
      <div id="contentIframe">
        <iframe src="about:blank" id="tableauFrame"></iframe>
        <div id="authMessage"></div>
      </div>
    </div>
    <div class="borderDiv" @click="handleSelect" @mousedown.stop="handlePreSelect" ref="menu">
      <span class="borderCorner"></span>
      <span cmd="add"><i class="el-icon-add-location"></i>add to menu</span>
      <span cmd="info"><i class="el-icon-info"></i>informaion</span>
      <span cmd="open"><i class="el-icon-open"></i>open</span>
    </div>
  </div>
</template>

<script>
  import bus from '../bus';
  import vTableauListItem from './TableauListItem'

  let $ = null
  export default {
    name: "tableau",
    components: {
      vTableauListItem
    },
    props: {
      /*userid:{
        type:String,
        default:null
      }*/
    },
    data() {
      return {
        userid: null,

        //data bind with the content items template
        listdata: [],

        //data bind with the breadcrumbs control template
        nav_items: [],

        //project ids are directly from server response
        project_by_ids: {},
        //converted to array and used by modal
        projects: null,
        //project_id: null,

        workbooks: null,
        workbook_by_ids: {},

        //a cache to save any used workbook's views and view ids
        workbook_views: {},

        //workbook_id: null,
        //the views of workbook_id
        views: null,
        //the view ids of workbook_id
        view_by_ids: {},

        //viewdepth=0: projects
        //viewdepth=1: workbooks of current project
        //viewdepth=2: views of current workbook
        //viewdepth=3: current view
        viewdepth: 0,

        //current project and workbook and view in the 'breadcrumb'
        project: null,
        workbook: null,
        view: null,

        current_query: {},

        //view_id: null,
        //baseurl: 'http://127.0.0.1:5000',
        baseurl: 'http://10.94.81.132:5000',

        loading: false,
        loadingMsg: '',
        //contains request and canceled=false
        lastRequest: null,

        current_menu_data: null
      }
    },

    methods: {
      show_error(msg, cb, args) {
        this.$confirm('The server has encountered an error: ' + msg + '. Click the "confirm" button to refresh.', 'Server', {
          confirmButtonText: 'confirm',
          cancelButtonText: 'cancel',
          type: 'warning',
          callback: action => {
            if (action == "confirm") {
              cb.apply(this, args)
            }
          }
        })
      },

      load_projects(success_cb) {
        if (this.projects != null) {
          if (success_cb != null) {
            success_cb()
          }
          return;
        }

        let that = this
        let request = $.ajax(this.baseurl + "/projects_data?userid=" + this.userid)
        let global_request = this.cancelRequest(request, "Loading project data...")
        request.done(function () {
          //alert(request.responseText)
          let result;
          eval("result = " + request.responseText);
          if (result.state == "succeeded") {
            let project_by_ids = result.projects

            let projects = []
            for (let pid in project_by_ids) {
              let project = project_by_ids[pid]
              project.id = pid
              projects.push(project)
            }

            that.project_by_ids = project_by_ids
            that.projects = projects
            if (success_cb != null) {
              success_cb()
            }
          } else if (result.state == "failed") {
            that.show_error(result.error, that.load_projects, arguments)
          } else {
            that.show_error("state=" + result.state, that.load_projects, arguments)
          }
        }).fail(function () {
          if (global_request.canceled) return;
          that.show_error("The request of /projects_data failed", that.load_projects, arguments)
        })
      },

      load_workbooks(success_cb) {
        if (this.projects == null) {
          let that = this;
          this.load_projects(function () {
            that.load_workbooks(success_cb)
          });
          return
        }

        if (this.workbooks != null) {
          //this.draw_projects(project_id);
          if (success_cb != null) {
            success_cb()
          }
          return;
        }

        let that = this
        let request = $.ajax(this.baseurl + "/workbooks_data?userid=" + this.userid)
        let global_request = this.cancelRequest(request, "Loading project data...")
        request.done(function () {
          //alert(request.responseText)
          let result;
          eval("result = " + request.responseText);
          if (result.state == "succeeded") {
            let workbooks = result.data
            let workbook_by_ids = {}
            let pids = that.project_by_ids
            for (let i of workbooks) {
              workbook_by_ids[i.id] = i;
              let pid = i.project_id
              let project = pids[pid]
              if (project == null) {
                project = pids[pid] = {}
                project.name = "<" + i.project_name + ">"
              }

              let children = null
              if ('children' in project) {
                children = pids[pid].children
              } else {
                children = pids[pid].children = []
              }

              children.push(i)
            }

            that.workbook_by_ids = workbook_by_ids
            that.workbooks = workbooks
            if (success_cb != null) {
              success_cb()
            }
          } else if (result.state == "failed") {
            that.show_error(result.error, that.load_workbooks, arguments)
          } else {
            that.show_error("state=" + result.state, that.load_workbooks, arguments)
          }
        }).fail(function () {
          if (global_request.canceled) return;
          that.show_error("The request of /workbooks_data failed", that.load_workbooks, arguments)
        })
      },

      draw_projects(project_id) {
        switch (typeof project_id) {
          case "object":
            if (project_id == null) {
              this.listdata = this.projects
            }
            break;

          case "function":
            //does not change listdata, download only.
            project_id()
            break;

          case "string":
            this.project_id = project_id;
            this.project = this.project_ids[project_id];
            this.listdata = this.project.children
            break;
        }
      },

      load_views(id, success_cb) {
        if (this.workbooks == null) {
          let that = this;
          this.load_workbooks(function () {
            that.load_views(id, success_cb)
          });
          return
        }

        //this.workbook_id = id;
        //this.workbook = this.workbook_ids[id]

        let cacheItem = this.workbook_by_ids[id]

        if (cacheItem != null && cacheItem.views != null) {
          //this.workbook = this.workbook_ids[id]
          //this.project = this.project_ids[this.workbook.project_id]
          //this.listdata = this.views
          this.view_by_ids = cacheItem.view_by_ids
          this.views = cacheItem.views
          if (success_cb != null) {
            success_cb()
          }
          return;
        }

        let that = this
        let request = $.ajax(this.baseurl + "/views_data?userid=" + this.userid + "&id=" + id)
        let global_request = this.cancelRequest(request, "Loading workbook data...")
        request.done(function () {
          //alert(request.responseText)
          let result;
          eval("result = " + request.responseText);
          if (result.state == "succeeded") {
            let views = result.data
            let view_by_ids = {}
            let cacheItem = {views: views, view_by_ids: view_by_ids}
            that.workbook_views[id] = cacheItem
            for (let i = 0; i < views.length; i++) {
              let view = views[i];
              view_by_ids[view.id] = view
            }
            //that.view_ids = view_ids;
            //that.workbook = that.workbook_ids[id]
            //that.project = that.project_ids[that.workbook.project_id]
            //that.listdata = that.views
            that.view_by_ids = view_by_ids
            that.views = views
            if (success_cb != null) {
              success_cb()
            }
          } else if (result.state == "failed") {
            that.show_error(result.error, that.load_views, arguments)
          } else {
            that.show_error("state=" + result.state, that.load_views, arguments)
          }
        }).fail(function () {
          if (global_request.canceled) return;
          that.show_error("The request of /views_data failed", that.load_views, arguments)
        })
      },

      //handle for 'refresh' button.
      handleRefresh() {
        //clear existing data of current viewdepth
        switch (this.viewdepth) {
          case 0:
            this.project_by_ids = {}
            this.projects = null

          case 1:
            this.workbooks = null
            this.workbook_by_ids = {}
            this.project = null
            this.workbook_views = {}

          case 2:
            this.views = null
            this.view_by_ids = {}
            this.workbook = null

          case 3:
            this.view = null
        }

        let that = this;
        this.refresh_current(function () {

          switch (that.viewdepth) {
            case 0:
              that.$message({
                message: 'Projects has been refreshed!',
                type: 'success'
              });
              break;

            case 1:
              that.$message({
                message: '(Current Project)' + that.project.name + ' has been refreshed!',
                type: 'success'
              });
              break;

            case 2:
              that.$message({
                message: '(Workbook)' + that.workbook.name + ' has been refreshed!',
                type: 'success'
              });
              break;

            case 3:
              that.$message({
                message: that.view.name + ' has been refreshed!',
                type: 'success'
              });
              break;

          }

        });
      },

      show_projects(success_cb) {
        //clear query string to point to 'projects'
        this.current_query = {}

        this.viewdepth = 0;

        //load project data,
        //  if success, show result.
        let that = this;
        this.load_projects(function () {
          that.close_iframe()
          that.listdata = that.projects;
          that.nav_items = [];
          success_cb()
        })
      },

      show_workbooks(success_cb) {
        //clear query string to point to one project
        this.current_query = {prj: this.current_query.prj}

        this.viewdepth = 1;

        this.close_iframe();
        this.listdata = this.project.children
        this.nav_items = [
          {title: this.project.name, path: '/tableau?prj=' + this.project.id}
        ];

        success_cb()
      },

      show_views(success_cb) {
        //clear query string to point to one workbook
        delete this.current_query['view']

        this.viewdepth = 2;

        this.close_iframe();
        this.listdata = this.views
        // the 'breadcrumb' items
        let prjpart = '/tableau?prj=' + this.project.id
        let wbpart = prjpart + "&wb=" + this.workbook.id
        this.nav_items = [
          {title: this.project.name, path: prjpart},
          {title: this.workbook.name, path: wbpart}
        ];

        success_cb()
      },

      show_tableau_view(success_cb) {
        this.viewdepth = 3;
        // change the 'breadcrumb' items before the content is visible
        let prjpart = '/tableau?prj=' + this.project.id
        let wbpart = prjpart + "&wb=" + this.workbook.id
        let viewpart = wbpart + "&view=" + this.view_id
        this.nav_items = [
          {title: this.project.name, path: prjpart},
          {title: this.workbook.name, path: wbpart},
          {title: this.view.name, path: viewpart}
        ];

        //show the loading page
        this.open_iframe()

        this.load_tableau_view(this.view.content_url, this.cb_success, this.cb_failure)

        success_cb()
      },

      refresh_current(success_cb) {
        if (success_cb == null) {
          success_cb = function () {
          }
        }
        //clear breadcrumbs data
        this.nav_items = []
        //clear items data
        this.listdata = []

        if (this.current_query.prj == null) {
          this.show_projects(success_cb);
        } else {
          let that = this
          this.load_workbooks(function () {
            let project = that.project_by_ids[that.current_query.prj]
            if (project == null) {
              that.show_projects(success_cb);
            } else {
              that.project = project;

              if (that.current_query.wb == null) {
                that.show_workbooks(success_cb);
              } else {
                let workbook = that.workbook_by_ids[that.current_query.wb]
                if (workbook == null || workbook.project_id != that.current_query.prj) {
                  that.show_workbooks(success_cb);
                } else {
                  that.workbook = workbook;
                  that.load_views(that.current_query.wb, function () {
                    if (that.current_query.view == null) {
                      that.show_views(success_cb)
                    } else {
                      let view = that.view_by_ids[that.current_query.view]
                      if (view == null) {
                        that.show_views(success_cb)
                      } else {
                        that.view = view;
                        that.show_tableau_view(success_cb)
                      }
                    }
                  })
                }
              }
            }
          })

        }
      },

      //handle for context menu item 'open'.
      handleShowMenu(data, ele) {
        console.log("open:" + data.id)
        this.current_menu_data = data;
        let jele = $(ele)
        //console.log("window:")
        //console.log(jele.offset())
        //console.log("parent:")
        //console.log(jele.position())
        //console.log("width:"+jele.width()+",height:"+jele.height())
        let pjele = jele.parent().parent()
        //console.log("parent width:"+pjele.width()+",height:"+pjele.height())
        let menu = $(this.$refs['menu'])
        let offset = jele.offset()
        menu.show().offset({left: (offset.left + jele.width()), top: offset.top})
      },

      handlePreSelect(event) {

      },

      handleSelect(event) {
        let type = event.target.attributes.cmd.nodeValue
        let menuele = this.$refs['menu']
        let menu = $(menuele)
        console.log(menuele)
        menu.hide();

        console.log(type)
        if (type != "open") {
          return
        }

        let id = this.current_menu_data.id;
        switch (this.viewdepth) {
          case 0:
            //enter level 0 or 1
            if (id) {
              this.current_query.prj = id;
              this.changeQuery({prj: this.current_query.prj})
            } else {
              this.current_query.prj = null;
            }

            console.log("view depth:0->" + this.viewdepth)
            this.refresh_current();

            break;

          case 1:
            //enter level 2
            this.current_query.wb = id;
            this.changeQuery({prj: this.current_query.prj, wb: this.current_query.wb})
            this.refresh_current();
            break;

          case 2:
            //enter level 3
            this.current_query.view = id;
            this.changeQuery({prj: this.current_query.prj, wb: this.current_query.wb, view: this.current_query.view})
            this.refresh_current();
        }
      },

      cb_success(that, actual_url) {
        $("#tableauFrame").attr("src", actual_url).css("visibility", "visible");
        $("#authMessage").css("visibility", "hidden")
      },
      cb_failure(that, msg) {
        $("#authMessage").css("visibility", "visible").html("<br /><br />Authentication failed: " + msg + ".  Please refresh this page!")
        $("#tableauFrame").css("visibility", "hidden");
      },
      load_tableau_view(url, success_cb, failure_cb) {
        let that = this
        let request = $.ajax(this.baseurl + "/get_token?userid=" + this.userid)
        let global_request = this.cancelRequest(request, "Loading view data...")
        request.done(function () {
          let result = null;
          eval("result = " + request.responseText)
          if (result.state == 'succeeded') {
            let options = "?:showVizHome=no&:embed=true&:showShareOptions=false&:toolbar=top&:tabs=no"
            let actual_url = result.url + "/trusted/" + result.token + "/views/" + url.replace("/sheets/", "/") + options
            if (success_cb) {
              success_cb(that, actual_url)
            }
          } else if (result.state == 'failed') {
            if (failure_cb) {
              failure_cb(that, "server failed to get ticket (" + result.error + ")")
            }
          } else {
            if (failure_cb) {
              failure_cb(that, "unknown response (state=" + result.state + ")")
            }
          }
        }).fail(function () {
          if (global_request.canceled) return;
          if (failure_cb) {
            failure_cb(that, "The request of '/get_token' failed.")
          }
        })
      },

      close_iframe() {
        $("#contentIframe").hide()
        //$("#tableauFrame").css("visibility", "hidden");
        //$("#authMessage").css("visibility", "hidden");
        $("#contentList").show()
      },

      open_iframe() {
        $("#tableauFrame").attr("src", "about:blank").css("visibility", "hidden")
        $("#authMessage").html("<br /><br />Downloading Authentication Token ...").css("visibility", "visible")
        let height1 = $("#idContentArea").height(), height2 = $("#idContentTableauHeader"), height = height1 - height2
        console.log(height1 + "-" + height2 + "=" + height)
        $("#contentIframe").show().css("height", height)
        $("#contentList").hide()
      },

      //change the content of browser address.
      //newQueryStr should be a js object {name:value, ...}
      changeQuery(newQueryStr) {
        let path = this.$router.history.current.path;
        this.$router.push({path: path, query: newQueryStr})
      },

      cancelRequest(newRequest, loadingMsg) {
        if (this.lastRequest != null) {
          let last = this.lastRequest
          if (last.canceled != true) {
            last.canceled = true;
            last.request.abort();
            if (newRequest == null) {
              this.loading = false;
              return null;
            }
          }
        }

        let ret = this.lastRequest = {
          request: newRequest,
          canceled: false
        }
        this.loading = true;
        this.loadingMsg = loadingMsg;
        let that = this;
        newRequest.done(function () {
          that.loading = false;
        }).fail(function () {
          that.loading = false;
        })
        return ret;
      },

      //ATTENTION: do not use the query object without copying a new one when passing to router.
      showUrl(queryStr) {
        let old_value = this.current_query;
        this.current_query = {...queryStr};
        let that = this;
        this.refresh_current(function () {
          console.log("old:" + old_value + ",new:" + queryStr + ",now:" + that.current_query)
          let path = that.$router.history.current.path;
          that.$router.replace({path: path, query: {...that.current_query}})
        });
      },

      is_query_changed(new_str) {
        let old_str = this.current_query;
        if (new_str.prj != old_str.prj
          || new_str.wb != old_str.wb
          || new_str.view != old_str.view
        )
          return true;
        else
          return false;
      }
    },

    watch: {
      $route() {
        console.log("watch url: ")
        let queryStr = this.$router.history.current.query
        console.log(queryStr)
        if (this.is_query_changed(queryStr)) {
          this.showUrl(queryStr)
        }
      }

    },

    mounted() {
      //this should be before url processing
      $ = this.jq
      //$(document).ready(function(){
      $("#contentIframe").hide()
      //})

      let userid = sessionStorage.getItem('tableau_backend_userid');
      if (userid == null) {
        this.$message.warning('Login required!');
        return
      } else {
        this.userid = userid
      }

      // console.log("url: ")
      let queryStr = this.$router.history.current.query
      // console.log(queryStr)
      this.showUrl(queryStr)

      let that = this;
      let menuele = this.$refs['menu']
      let menu = $(menuele)
      // console.log(menuele)
      menu.hide();
      //menu.css({display:"none"});

      let w = $(window);
      if (window.w_resize != null) {
        w.unbind('resize', window.w_resize)
      }
      window.w_resize = function () {
        if (that.viewdepth == 3) {
          let height1 = $("#idContentArea").height(), height2 = $("#idContentTableauHeader"), height = height1 - height2
          console.log(height1 + "-" + height2 + "=" + height)
          $("#contentIframe").css("height", height)
        }
      }
      w.resize(window.w_resize)

      let b = $(document.body)
      if (window.b_mousedown != null) {
        b.unbind('mousedown', window.b_mousedown)
      }
      window.b_mousedown = function (event) {
        console.log("body mousedown")
        menu.hide();
      }
      b.mousedown(window.b_mousedown)

      bus.$on('userinfo_changed', new_value => {
        that.userid = new_value.id;
        if (that.userid == null) {
          that.close_iframe();
          that.listdata = null;
          that.nav_items = [];
        } else {
          let queryStr = {}
          if (that.is_query_changed(queryStr)) {
            that.changeQuery({})
          } else {
            that.refresh_current();
          }
        }
      });
    }
  }

</script>
<style scoped>
  .breadcrumbs a:hover {
    border-bottom: 1px solid blue;
  }

  .breadcrumbs a:active {
    color: #BC8F8F;
    border-bottom: 1px solid #BC8F8F;
  }

  .breadcrumbs .sep {
    margin-left: 10px;
    margin-right: 10px;

  }

  .breadcrumbs {
    margin-left: 20px
  }

  div.main-content {
    position: relative;
    width: 100%;
    margin-top: 10px;
  }

  /*used by contentIframe*/
  .tableau-view {
    width: 100%;
    height: 100%;
  }

  .main-content {
    width: 100%;
    height: 100%
  }

  .main-content .container {
    display: flex;
    flex-wrap: wrap;
    background: #F0FFFF;
  }

  .main-content #contentIframe {
    position: relative;
    overflow: hidden;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%
  }

  .main-content #tableauFrame {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%
  }

  .main-content #authMessage {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    font-size: 2em;
    background: #eeeeee
  }


  .borderDiv > span[cmd] {
    display: block;
    font-size: 16px;
    height: 32px;
    line-height: 32px;
    padding: 0 !important;
    overflow: hidden;
    user-select: none;
  }

  .borderDiv > span[cmd]:hover {
    cursor: pointer;
    background-color: #87CEFA;
  }

  .borderDiv > span[cmd] > i {
    margin-right: 5px;
  }

  .borderCorner {
    position: absolute;
    left: -10px;
    top: 12px;
    width: 0;
    height: 0;
    overflow: hidden;
  / / border-left-width: 0;
  / / border: 6 px;
    border: 4px solid transparent;
    border-right: 6px solid transparent;
    border-right-color: #FFF;

  }

  .borderDiv {
    position: absolute;
    padding: 8px;
    width: 120px;
    height: 100px;
    border: 1px solid #EBEEF5;
    border-radius: 4px;
  / / box-shadow: 0 2 px 12 px 0 rgba(0, 0, 0, .1);
    filter: drop-shadow(0 2px 12px rgba(0, 0, 0, 0.1));
    left: 200px;
    top: 100px;
    background: white;
  }

</style>
