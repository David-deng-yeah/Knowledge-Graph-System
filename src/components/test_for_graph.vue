<!--<script src="../../../canvas_nest-master/test-clear.js"></script>-->
<template>
  <div>
    <div id="cy">
    </div>
    <div class="panel">
      <el-button @click="show = !show" size="mini" type="text">
        <i :class="show?'el-icon-arrow-right':'el-icon-arrow-left'"/>
      </el-button>
      <div v-if="show">
        <el-input v-model="cdn" placeholder="请输入报关单号" style="width: 150px"></el-input>
        <!--        点击搜索，执行on_go方法-->
        <el-button @click="on_go">搜索</el-button>
        <br>
        <!--        slider,改变边的长度-->
        <span>Edge Length</span>
        <el-slider v-model="vLength" @change="changeEdgeLength" :show-tooltip="false" :max="maxEdgeLength"
                   :min="minEdgeLength"></el-slider>
        <!--        slider,改变节点大小-->
        <span>Node Spacing</span>
        <el-slider v-model="vSpacing" @change="changeNodeSpacing" :show-tooltip="false" :max="maxNodeSpacing"
                   :min="minNodeSpacing"></el-slider>
        <br>
        <div v-for="(color,index) of colors" :key=index>
          <!--          一排按钮，控制节点的显示-->
          <el-switch v-model="values[index]" :active-color="color" :active-text="labels[index]"
                     @change="hideNodes(values[index], color, index)"></el-switch>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import cytoscape from "cytoscape";
import cola from "cytoscape-cola";
import jquery from 'jquery';
import panzoom from 'cytoscape-panzoom';
import contextMenus from 'cytoscape-context-menus';

try {
  // register extension
  cytoscape.use(panzoom, jquery);
  cytoscape.use(contextMenus, jquery);
  cytoscape.use(cola);
} catch (ex) {
  alert(ex)
}

//import CSS as well
import 'cytoscape-panzoom/cytoscape.js-panzoom.css';
// import 'cytoscape-navigator/cytoscape.js-navigator.css';
import 'cytoscape-context-menus/cytoscape-context-menus.css';

let cy;
let eles = [eles1, eles2, eles3, eles4, eles5, eles6, eles7, eles8, eles9, eles10, eles11, eles12, eles13, eles14];
let eles1, eles2, eles3, eles4, eles5, eles6, eles7, eles8, eles9, eles10, eles11, eles12, eles13, eles14;
// let removed;
// let hidden;
let init_nodeSpacing = 10;
let init_edgeLength = 100;
let layout_params =
    {
      name: 'cola',
      nodeSpacing: init_nodeSpacing,
      edgeLength: init_edgeLength,
      animate: true,
      randomize: false,
      maxSimulationTime: 1500
    };
let layout;

//创建布局
function makeLayout(opts) {
  if (!cy) return;
  layout_params.randomize = false;
  // layout_params.edgeLength = function (e) {
  //   let _weight = e.data('weight') || 0;
  //   if (_weight > 0 || _weight < 0)
  //     return layout_params.edgeLengthVal / e.data('weight');
  //   else return layout_params.edgeLengthVal //TODO find more later
  // };
  for (let i in opts) {
    layout_params[i] = opts[i];
  }
  return cy.layout(layout_params);
}

// let o2o = (o1 = {}, o2 = {}) => {
//   for (let k in o2) {
//     o1[k] = o2[k];
//   }
//   return o1;
// }

let gData = {
  raw: {},
  vToggleSlider: true,
  vLength: init_edgeLength,
  vSpacing: init_nodeSpacing,
  maxEdgeLength: 200,
  minEdgeLength: 0,
  maxNodeSpacing: 50,
  minNodeSpacing: 0,
  cdn: '010120200000122634',
  show: true,
  values: [true, true, true, true, true, true, true, true, true, true, true, true, true, true],
  colors: ['red', 'yellow', 'blue', 'antiquewhite', 'aquamarine', 'blueviolet', 'coral', 'darkturquoise', 'grey', 'deeppink', 'gainsboro', 'gold', 'lawngreen', 'orangered'],
  labels: ['报关单号', '舱单号', '查验任务编号', '经营/申报/货主单位代码', '经营/申报单位法人证件号', '贸易方式', '时间信息', '车辆信息', '进出口标记', '当班科室', '口岸当班科室', '布控信息', '查验信息', '机检信息']
}

// let env = 0;//0 dev 1 live
// let url_data_source = env ?
//     'http://10.94.81.132/todo' : 'http://10.94.81.132:5000/neo4j.main_graph'

// let fn_process_data = async ({style = 0}) => {
//   //TODO in data source out style 0 for [data{group,...}] 1 for {edges[], nodes[]}
//   let rt
//   return rt
// }

// let tableau_root = 'http://10.94.81.132';
//let tableau_root = 'http://127.0.0.1';
// let $ = k => document.all[k];


// 迁移过来的小api
// let o2s=(o)=>{ try{ return JSON.stringify(o) }catch(ex) {console.log('error')} }
// let s2o=(s)=>{ try{ return JSON.parse(s) } catch(ex){console.log('error')} }
// let json_api = (u,a,m,cb)=>{
//   let _cb = s=>(cb||console.log)(s2o(s),s);
//   let x = new XMLHttpRequest();
//   x.onreadystatechange=()=>(x.readyState==4)?_cb(x.responseText):null;
//   x.onerror=(e)=>_cb(e);
//   x.open(m,u,true);
//   x.setRequestHeader('Accept', 'application/json');
//   //x.setRequestHeader('Content-Type', 'application/json');
//   x.send(a);
//   return x;
// }

let init_cy = async (eles) => {
  try {
    // if (eles) localStorage.setItem('last_search_graph', o2s(eles));//save for quick load next round
    cy = window.cy = cytoscape({
      container: document.getElementById('cy'),
      elements: eles,
      style: cytoscape.stylesheet()//调整样式
          .selector('node')//节点样式
          .style({
            "width": 24, "height": 24,//节点的大小
            "content": "data(name)",
            "font-size": "9px",
            "text-valign": "center",
            "text-halign": "center",
            "background-color": "data(color)",
            "text-outline-color": "#555",
            "text-outline-width": "2px",
            "color": "#fff",
            "overlay-padding": "6px",
            "z-index": "10"
          })
          .selector('edge')//边样式
          .style({
            content: (ele) => ele.data('name'),
            "curve-style": "haystack",
            "haystack-radius": "0.5",
            "opacity": "0.4",
            "line-color": "#bbb",
            //"width": "mapData(weight, 0, 1, 1, 8)",
            "font-size": "9px",
            "width": 3,
            "overlay-padding": "3px"
          }),
      layout: layout_params,
    });

    // panzoom初始化
    // the default values of each option are outlined below:
    let panzoom_defaults = {
      zoomFactor: 0.05, // zoom factor per zoom tick
      zoomDelay: 45, // how many ms between zoom ticks
      minZoom: 0.1, // min zoom level
      maxZoom: 10, // max zoom level
      fitPadding: 50, // padding when fitting
      panSpeed: 10, // how many ms in between pan ticks
      panDistance: 10, // max pan distance per tick
      panDragAreaSize: 75, // the length of the pan drag box in which the vector for panning is calculated (bigger = finer control of pan speed and direction)
      panMinPercentSpeed: 0.25, // the slowest speed we can pan by (as a percent of panSpeed)
      panInactiveArea: 8, // radius of inactive area in pan drag box
      panIndicatorMinOpacity: 0.5, // min opacity of pan indicator (the draggable nib); scales from this to 1.0
      zoomOnly: false, // a minimal version of the ui only with zooming (useful on systems with bad mousewheel resolution)
      fitSelector: undefined, // selector of elements to fit
      animateOnFit: function () { // whether to animate on fit
        return false;
      },
      fitAnimationDuration: 1000, // duration of animation on fit

      // icon class names
      sliderHandleIcon: 'fa fa-minus',
      zoomInIcon: 'fa fa-plus',
      zoomOutIcon: 'fa fa-minus',
      resetIcon: 'fa fa-expand'
    };
    cy.panzoom(panzoom_defaults);

    // let contextMenu = cy.contextMenus({
    //   // Customize event to bring up the context menu
    //   // Possible options https://js.cytoscape.org/#events/user-input-device-events
    //   evtType: 'cxttap',
    //   // List of initial menu items
    //   // A menu item must have either onClickFunction or submenu or both
    //   menuItems: [
    //     {
    //       id: 'remove',
    //       content: 'remove',
    //       selector: 'node, edge',
    //       // onClickFunction: function (event) {
    //       //   // let target = event.target || event.cyTarget;
    //       //   // removed = target.remove();
    //       //
    //       //   contextMenu.showMenuItem('undo-last-remove');
    //       // },
    //       hasTrailingDivider: true
    //     },
    //     {
    //       id: 'undo-last-remove',
    //       content: 'undo last remove',
    //       selector: 'node, edge',
    //       show: false,
    //       coreAsWell: true,
    //       // onClickFunction: function (event) {
    //       //   if (removed) {
    //       //     removed.restore();
    //       //   }
    //       //   contextMenu.hideMenuItem('undo-last-remove');
    //       // },
    //       hasTrailingDivider: true
    //     },
    //     {
    //       id: 'hide',
    //       content: 'hide',
    //       selector: '*',
    //       // onClickFunction: function (event) {
    //       //   // let target = event.target || event.cyTarget;
    //       //   // hidden = target.hide();
    //       //   contextMenu.showMenuItem('show');
    //       // },
    //       disabled: false
    //     },
    //     {
    //       id: 'show',
    //       content: 'show',
    //       selector: '*',
    //       show: false,
    //       coreAsWell: true,
    //       // onClickFunction: function (event) {
    //       //   if (hidden) {
    //       //     hidden.show();
    //       //   }
    //       //   contextMenu.hideMenuItem('show');
    //       // }
    //     }
    //   ],
    //   // css classes that menu items will have
    //   menuItemClasses: [
    //     // add class names to this list
    //     'custom-menu-item'
    //   ],
    //   // css classes that context menu will have
    //   contextMenuClasses: [
    //     // add class names to this list
    //     'custom-context-menu'
    //   ],
    //   // Indicates that the menu item has a submenu. If not provided default one will be used
    //   submenuIndicator: {src: 'assets/submenu-indicator-default.svg', width: 12, height: 12}
    // });

    // 让makeout跑起来
    setTimeout(function () {
      layout = makeLayout();
      layout.run();
    }, 333)
  } catch (ex) {
    alert(ex)
  }
}


//这是一个vue object，可以导出成模块
export default {
  name: "ui_test",
  data: () => gData,//匿名函数
  // 异步初始化
  async mounted() {
    await init_cy(null);//初始化
  },
  methods: {
    // toggleStyle() {
    //   alert('TODO toggleStyle')
    // },
    //修改边的长度
    changeEdgeLength(e) {
      layout_params.edgeLength = e;
      if (layout) layout.stop()
      layout = makeLayout();
      layout.run();
    },
    //修改节点大小
    changeNodeSpacing(v) {
      layout_params.nodeSpacing = v;
      if (layout) layout.stop()
      layout = makeLayout();
      layout.run();
    },
    //调用初始化方法
    //数据格式 "node":[{},{},{}]

    // 节点的格式 id和name和color
    // 边格式 source和target和name
    on_go() {
      // 静态数据代码
      let init_data = {
        "nodes": [{
          "data": {
            "id": 14744,
            "name": "",
            "key": "",
            "val": "",
            "color": "gainsboro"
          }
        }, {
          "data": {
            "id": 4368,
            "name": "查验科长 林勉5301261",
            "key": "查验科长",
            "val": "林勉5301261",
            "color": "lawngreen"
          }
        }, {
          "data": {
            "id": 2188,
            "name": "中控时间 2020-03-25 14:25:55",
            "key": "中控时间",
            "val": "2020-03-25 14:25:55",
            "color": "coral"
          }
        }, {
          "data": {
            "id": 4,
            "name": "舱单号 5100282478089",
            "key": "舱单号",
            "val": "5100282478089",
            "color": "yellow"
          }
        }, {
          "data": {
            "id": 93370,
            "name": "人工查验主查人员 马永平5336870",
            "key": "人工查验主查人员",
            "val": "马永平5336870",
            "color": "lawngreen"
          }
        }, {
          "data": {
            "id": 7098,
            "name": "经营单位代码 1105919117",
            "key": "经营单位代码",
            "val": "1105919117",
            "color": "antiquewhite"
          }
        }, {
          "data": {
            "id": 33855,
            "name": "贸易方式 其他",
            "key": "贸易方式",
            "val": "其他",
            "color": "blueviolet"
          }
        }, {
          "data": {
            "id": 68796,
            "name": "进出口标记 出口",
            "key": "进出口标记",
            "val": "出口",
            "color": "grey"
          }
        }, {
          "data": {
            "id": 4915,
            "name": "申报单位代码 1105919117",
            "key": "申报单位代码",
            "val": "1105919117",
            "color": "antiquewhite"
          }
        }, {
          "data": {
            "id": 2736,
            "name": "申报时间 2020-03-24 14:39:56",
            "key": "申报时间",
            "val": "2020-03-24 14:39:56",
            "color": "coral"
          }
        }, {
          "data": {
            "id": 546,
            "name": "人工查验辅查人员 530126",
            "key": "人工查验辅查人员",
            "val": "530126",
            "color": "lawngreen"
          }
        }, {
          "data": {
            "id": 16932,
            "name": "报关单号 010120200000122634",
            "key": "报关单号",
            "val": "010120200000122634",
            "color": "red"
          }
        }, {
          "data": {
            "id": 40408,
            "name": "进出境时间 2020-03-25 11:03:22",
            "key": "进出境时间",
            "val": "2020-03-25 11:03:22",
            "color": "coral"
          }
        }, {
          "data": {
            "id": 102102,
            "name": "布控人代码 0119450",
            "key": "布控人代码",
            "val": "0119450",
            "color": "gold"
          }
        }, {
          "data": {
            "id": 89548,
            "name": "派单时间 2020-03-25 11:26:44",
            "key": "派单时间",
            "val": "2020-03-25 11:26:44",
            "color": "coral"
          }
        }, {
          "data": {
            "id": 68800,
            "name": "车牌号 粤ZEN75港",
            "key": "车牌号",
            "val": "粤ZEN75港",
            "color": "darkturquoise"
          }
        }, {
          "data": {
            "id": 9286,
            "name": "查验任务编号 530120200500441589",
            "key": "查验任务编号",
            "val": "530120200500441589",
            "color": "blue"
          }
        }, {
          "data": {
            "id": 1093,
            "name": "货主单位代码 1111949997",
            "key": "货主单位代码",
            "val": "1111949997",
            "color": "antiquewhite"
          }
        }, {
          "data": {
            "id": 52964,
            "name": "司机ID 53147426",
            "key": "司机ID",
            "val": "53147426",
            "color": "darkturquoise"
          }
        }],

        "edges": [
            {"data": {"source": 4, "target": 16932, "name": ["舱单_报关单"]}}, {
          "data": {
            "source": 4,
            "target": 68800,
            "name": ["舱单_车牌号"]
          }
        }, {"data": {"source": 9286, "target": 4368, "name": ["查验编号_查验科长"]}}, {
          "data": {
            "source": 9286,
            "target": 2188,
            "name": ["查验编号_中控时间"]
          }
        }, {"data": {"source": 9286, "target": 93370, "name": ["查验编号_查验主查"]}}, {
          "data": {
            "source": 9286,
            "target": 4,
            "name": ["查验编号_舱单"]
          }
        }, {"data": {"source": 9286, "target": 89548, "name": ["查验编号_派单时间"]}}, {
          "data": {
            "source": 9286,
            "target": 546,
            "name": ["查验编号_查验辅查"]
          }
        }, {"data": {"source": 9286, "target": 102102, "name": ["查验编号_布控人"]}}, {
          "data": {
            "source": 4,
            "target": 40408,
            "name": ["舱单_进出境时间"]
          }
        }, {"data": {"source": 4, "target": 52964, "name": ["舱单_司机"]}}, {
          "data": {
            "source": 16932,
            "target": 2736,
            "name": ["报关单_申报时间"]
          }
        }, {"data": {"source": 16932, "target": 4, "name": ["报关单_舱单"]}}, {
          "data": {
            "source": 16932,
            "target": 1093,
            "name": ["报关单_货主单位"]
          }
        }, {"data": {"source": 16932, "target": 9286, "name": ["报关单_查验任务"]}}, {
          "data": {
            "source": 9286,
            "target": 16932,
            "name": ["查验编号_报关单"]
          }
        }, {"data": {"source": 16932, "target": 33855, "name": ["报关单_贸易方式"]}}, {
          "data": {
            "source": 16932,
            "target": 14744,
            "name": ["报关单_口岸当班科室"]
          }
        }, {"data": {"source": 16932, "target": 68796, "name": ["报关单_进出口标记"]}}, {
          "data": {
            "source": 16932,
            "target": 7098,
            "name": ["报关单_经营单位"]
          }
        }, {"data": {"source": 16932, "target": 4915, "name": ["报关单_申报单位"]}}]
      };
      //初始化数据
      init_cy(init_data);

      // 原来的代码
      // let get_a = () => ({"报关单号": gData.cdn});
      // json_api(tableau_root + ':5000/neo4j.post_graph', o2s(get_a()), 'POST',
      //     (o, s) => {
      //       if (!o) return alert(s)
      //       init_cy(o);
      //     })
    },
    //隐藏节点(按掉某些按钮，隐藏某些节点)
    hideNodes(v, c, i) {
      let collection = cy.elements(`node[color='${c}']`);
      if (!v) {
        eles[i] = collection.hide();
      } else {
        eles[i].show();
      }
    }
  }
}
</script>

<style scoped>
#cy {
  height: 100%;
  width: 100%;
  position: absolute;
  left: 0;
  z-index: 0;
}

/*搜索框，按钮排的css*/
.panel {
  position: absolute;
  font-size: 80%;
  line-height: 25px;
  right: 20px;
  margin-top: 10px;
  margin-bottom: 10px;
  z-index: 1;
}

/*.fade-enter-active, .fade-leave-active {*/
/*  transition: opcity .5s;*/
/*}*/
/*.fade-enter, .fade-leave-to {*/
/*  opacity: 0;*/
/*}*/

</style>
