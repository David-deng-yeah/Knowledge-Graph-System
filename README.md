# 一、架构
*    前端：Vue + Element UI
*    后端：Flask + Mysql

貌似有两个数据库：dba是mysql，dba2是gbase
|-- dba
  |--dba.py main类负责连接数据库，并可以通过dosql函数执行sql查询，并返回结果
  |--mysql-proxy.lua 中间层
|--node_modules
|--src
|--static
|--neo4j.py 连接neo4j数据库，根据输入的商品编号，返回对应的节点信息。进行数据预处理
|--flsk.py 后端程序（感觉和main.py功能很像，不知道有什么用。。）
|--logic.py 前端通过调用此函数的get_routers方法获取数据表中的路由信息，并在侧边生成对应的菜单，并且可以对数据表进行curd
|--global_variable.py 全局变量

tableau后端服务器的ip为：'http://10.94.81.132'
DBA：数据库助手
web.tmp：数据表
tsc：tableau相关
## 1.1逻辑结构
#### 登录
前端通过调用main.py中的login接口，发送用户名和密码，后端收到请求，验证用户名和密码，验证成功就返回给前端userid, username, token，前端拿到后将userid和username临时存储到sessionStorage中，并跳转到对应的路由页面。

#### 报关单图谱查询
后端通过neo4j.py中的buildNodes和buildEdges函数对节点和边的信息进行预处理，添加颜色属性等。前端通过post请求调用neo4j.py中的post_graph方法继而调用_main_graph函数获得节点和边的数据，并在前端通过json_api和o2s将数据转为json格式，并且通过init_cy方法进行报关单图谱的渲染。并且将上次查询结果保存在localStorage中，方便下次打开时直接渲染上次的结果。

#### 动态路由
前端通过调用logic.py中的get_routers方法获取数据表中的路由信息，返回一个json格式的路由表，并根据路由表中的信息在侧边菜单栏生成对应的菜单。并且在配置路由页面可通过调用logic.py中的routers_show,routers_insert,routers_delete,routers_update方法来实现对数据表的CRUD，从而实现在前端对路由的配置。
```json
{
  "router": [
    {
      "path": "/trend_dev",
      "component": "tableau_view",
      "meta": {
        "title": "\u6df1\u5733\u5173\u533a\u9646\u8def\u53e3\u5cb8\u8fdb\u51fa\u53e3\u6001\u52bf",
        "url": "/views/_0/sheet0?:showAppBanner=false&:origin=viz_share_link&:display_count=n&:showVizHome=n"
      }
    }
  ]
}
```

#### Tableau view权限管理
前端通过logic.py中的check_view方法获取view_id，若返回值为null则无权限，展示403页面，反之截取url中的sheet_id字段获取content_url，并拼接成完整的url，展示tableau view页面。

## 1.2目录结构
```
```
### 1.2.1功能
-    [x] Login/Logout
-    [x] Tableau Workbook
-    [x] 报关单图谱
-    [x] Tableau View
-    [x] 配置路由(管理员权限)
-    [x] 混编框架
### 1.2.2具体功能及其使用
####报关单图谱
输入报关单号可查询该报关单号及其上下文的所有信息，右侧的Edge Length和Node Spacing可调节边的长度和节点的位置，Legend为Toggle，点击可隐藏该颜色对应的所有节点及其连接的边，再次点击可恢复。左侧为panzoom，可进行缩放及画布自适应。

#### Tableau View
所有Tableau View共用一个component，在目录src/components/TableauViewIframe.vue中，通过logic.check_view来判断用户是否有权限访问该视图，若有权限则展示tableau view中的内容，若无权限则展示src/components/403.vue中的内容。

#### 配置路由
可直接在管理员权限下级菜单配置路由中添加或修改路由的相关信息，点击提交后该信息会自动保存到数据表web.tmp中,每次登录时，会自动获取数据表中的路由信息，动态加载路由和左侧菜单。

#### 混编框架
通过Tableau js API实现对视图的一系列操作，包括Filter, Select等等。
```
viz = new tableau.Viz(containerDiv, url, options);
options有多个可选参数，例如hideToolbar, hideHeader, hideTabs等等，之后进行tableau view设置时可在此修改。

```
# 二、典型调用序列
# 三、关键代码说明
#### TableauViewIframe.vue
这里采用iframe来展示tableau的视图，先给iframe一个默认的空白页作为src，然后通过read_from_router方法获取需要数据表中的url，然后通过change_url函数验证权限并且拿到token，然后拼接出完整的tableau view的url去替换空白页。
```vue
<template>
  <!-- <v-for a_frame><iframe src= a_frame[k] ...</v-for> -->
  <iframe
    :key="trigger_update_url"
    :src="view_url"
    frameborder="0" width="100%" height="100%">
  </iframe>
</template>

<script>
  let my_url;
  export default {
    name: "analysis",
    data() {
      return {
        view_url: ''
      }
    },
    computed: {
      trigger_update_url() {
        this.view_url = "about:blank";
        this.change_url()
        return this.$route.meta.url;
      }
    },
    methods: {
      read_from_router() {
        // console.log(this.$route.meta.url);
        return this.$route.meta.url;
      },
      async change_url() {
        let url = this.read_from_router();
        let end = url.indexOf("?");
        // console.log(end);
        let content_url = url.substring(7, end);
        // console.log(content_url);
        let username = sessionStorage.getItem('tableau_backend_username');
        // console.log(username);
        let auth = await (await fetch('http://10.94.81.132:5000/logic.check_view?username=' + username + '&content_url=' + content_url)).json();
        // console.log(auth.view);
        if (auth.view) {
          let userid = sessionStorage.getItem('tableau_backend_userid');
          // console.log(userid);
          let token_o = await (await fetch('http://10.94.81.132:5000/get_token?userid=' + userid)).json();
          if (token_o) {
            //old(need login with cookie save): url = "http://10.94.81.132/views/_0/sheet0?:showAppBanner=false&:origin=viz_share_link&:display_count=n&:showVizHome=n",
            //e.g. http://10.94.81.132/trusted/TqzPvNviQKSIw4aoHpDI-Q==:AUj8fPbWaUnXnupipU60baIf/views/_0/sheet0?:showVizHome=no&:embed=true&:showShareOptions=false&:toolbar=top&:tabs=no

            my_url = `${token_o.url}/trusted/${token_o.token}${url}`;
            // console.log(token_o.url);
            this.view_url = my_url;

            // console.log("111", token_o);
          } else {
            //TODO sess expired?
            // console.log("222", token_o);
          }
          // return my_url;
        }
        else {
          this.view_url = 'http://10.94.81.132:8080/403';
        }
      }
    },
    async mounted() {
    }
  }
</script>

<style scoped>

</style>

```
#### CustomsDeclarationGraph.vue
输入报关单号点击搜索按钮后触发on_go方法，post请求获取数据然后调用init_cy函数进行页面的渲染。
```
  let init_cy = async (eles) => {
    try {
      if (eles) localStorage.setItem('last_search_graph', o2s(eles));//save for quick load next round
        cy = window.cy = cytoscape({
        container: document.getElementById('cy'),
        elements: eles? eles : s2o(localStorage.getItem('last_search_graph')),
        style: cytoscape.stylesheet()
        layout: layout_params,
      });
      setTimeout(function () {
        //if(layout) layout.stop()
        layout = makeLayout();
        layout.run();
      }, 333)
    }
    catch (ex) {
      alert(ex)
    }
  }
  on_go() {
    let get_a = () => ({"报关单号": gData.cdn});
    json_api(tableau_root + ':5000/neo4j.post_graph', o2s(get_a()), 'POST',
      (o, s) => {
        if (!o) return alert(s)
        init_cy(o);
      })
  }
```

# 四、DB设计，数据表说明
本项目中数据信息比较简单，在数据库web下只创建了一张存储路由信息的数据表tmp，该数据表一共有8个字段，分别为id, parent_id, self_key, parent_key, path, component, title, url。其中parent_key可为null。
```
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
| srt          | float        | NO   |     | NULL    |                |
| self_key     | varchar(100) | NO   |     | NULL    |                |
| parent_key   | varchar(100) | YES  |     | NULL    |                |
| path         | varchar(40)  | NO   |     | NULL    |                |
| component    | varchar(40)  | NO   |     | NULL    |                |
| title        | varchar(100) | NO   |     | NULL    |                |
| url          | varchar(100) | NO   |     | NULL    |                |
| db           | varchar(40)  | YES  |     | NULL    |                |
| sql_sentence | text         | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
```

# 五、配置页面使用说明
## 5.1 配置路由
如果需要新增路由，则点击ADD按钮，然后填写路由信息，最后点击SUBMIT按钮；如果需要修改路由，则点击EDIT按钮，然后修改路由信息，最后点击SUBMIT按钮；如果需要删除路由，则只需点击该行对应的DELETE按钮。路由信息表中SRT为路由信息的顺序，类型为float，可修改SRT的值来改变菜单和路由信息表中对应项的位置。路由信息表中SELF_KEY, PATH, COMPONENT, TITLE, URL为必填项，PARENT_KEY, DB, SQL_SENTENCE为可选项，默认为null。

## 5.2 配置混编页面
如果需要添加混编页面，则首先打开配置混编页面的页面，然后选择数据库，输入sql语句，点击查询，可以预览查询到的数据表的内容。然后输入Tableau视图的链接，点击查询，可以预览查询到的Tableau视图的内容，如果确认无误则点击保存按钮，然后填写对应的路由信息，最后点击确定即可。

## 5.3 修改已添加的混编页面的URL, DB, SQL信息
如果想要更换或修改已添加的混编页面的Tableau视图，数据库和查询到的数据表的信息，则在左侧菜单栏找到想要修改的混编页面，点击跳转到该混编页面，然后点击修改按钮，修改URL, DB, SQL信息，点击确定即可。
