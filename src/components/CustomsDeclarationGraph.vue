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
        <el-button @click="on_go">搜索</el-button>
        <br>
        <span>Edge Length</span>
        <el-slider v-model="vLength" @change="changeEdgeLength" :show-tooltip="false" :max="maxEdgeLength"
                   :min="minEdgeLength"></el-slider>
        <span>Node Spacing</span>
        <el-slider v-model="vSpacing" @change="changeNodeSpacing" :show-tooltip="false" :max="maxNodeSpacing"
                   :min="minNodeSpacing"></el-slider>
        <br>
        <div v-for="(color,index) of colors">
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

// import CSS as well
import 'cytoscape-panzoom/cytoscape.js-panzoom.css';
// import 'cytoscape-navigator/cytoscape.js-navigator.css';
import 'cytoscape-context-menus/cytoscape-context-menus.css';

let cy;
let eles = [eles1, eles2, eles3, eles4, eles5, eles6, eles7, eles8, eles9, eles10, eles11, eles12, eles13, eles14];
let eles1, eles2, eles3, eles4, eles5, eles6, eles7, eles8, eles9, eles10, eles11, eles12, eles13, eles14;
let removed;
let hidden;
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

let o2o = (o1 = {}, o2 = {}) => {
  for (let k in o2) {
    o1[k] = o2[k];
  }
  return o1;
}
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
let env = 0;//0 dev 1 live
let url_data_source = env ?
  'http://10.94.81.132/todo' : 'http://10.94.81.132:5000/neo4j.main_graph'

let fn_process_data = async ({style = 0}) => {
  //TODO in data source out style 0 for [data{group,...}] 1 for {edges[], nodes[]}
  let rt
  return rt
}

let tableau_root = 'http://10.94.81.132';
let $ = k => document.all[k];


//eles为从neo4j读出来的数据，直接赋值给cy的elements
let init_cy = async (eles) => {
  try {
    if (eles) localStorage.setItem('last_search_graph', o2s(eles));//save for quick load next round
    cy = window.cy = cytoscape({
      container: document.getElementById('cy'),
      //将result赋值给element
      elements: eles ? eles : s2o(localStorage.getItem('last_search_graph')),
      //elements: j,
      //style:stl,
      style: cytoscape.stylesheet()
        //设计节点样式
        .selector('node')
          .style({
            //"width": "mapData(score, 0, 0.006769776522008331, 20, 60)",
            //"height": "mapData(score, 0, 0.006769776522008331, 20, 60)",
            "width": 24, "height": 24,
            "content": "data(name)",//节点内容为data的name
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
        //设计边的样式
        .selector('edge')
          .style({
            content: (ele) => ele.data('relation'),//边的内容
            "curve-style": "haystack",
            "haystack-radius": "0.5",
            "opacity": "0.4",
            "line-color": "#bbb",
            //"width": "mapData(weight, 0, 1, 1, 8)",
            "font-size": "9px",
            "width": 3,
            "overlay-padding": "3px"
          }),
      //layout: {name: 'cola'},
      layout: layout_params,
    });
    // panzoom
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
    // add the panzoom control
    cy.panzoom(panzoom_defaults);
    let contextMenu = cy.contextMenus({
      // Customize event to bring up the context menu
      // Possible options https://js.cytoscape.org/#events/user-input-device-events
      evtType: 'cxttap',
      // List of initial menu items
      // A menu item must have either onClickFunction or submenu or both
      menuItems: [
        {
          id: 'remove',
          content: 'remove',
          selector: 'node, edge',
          onClickFunction: function (event) {
            let target = event.target || event.cyTarget;
            removed = target.remove();

            contextMenu.showMenuItem('undo-last-remove');
          },
          hasTrailingDivider: true
        },
        {
          id: 'undo-last-remove',
          content: 'undo last remove',
          selector: 'node, edge',
          show: false,
          coreAsWell: true,
          onClickFunction: function (event) {
            if (removed) {
              removed.restore();
            }
            contextMenu.hideMenuItem('undo-last-remove');
          },
          hasTrailingDivider: true
        },
        {
          id: 'hide',
          content: 'hide',
          selector: '*',
          onClickFunction: function (event) {
            let target = event.target || event.cyTarget;
            hidden = target.hide();
            contextMenu.showMenuItem('show');
          },
          disabled: false
        },
        {
          id: 'show',
          content: 'show',
          selector: '*',
          show: false,
          coreAsWell: true,
          onClickFunction: function (event) {
            if (hidden) {
              hidden.show();
            }
            contextMenu.hideMenuItem('show');
          }
        }
      ],
      // css classes that menu items will have
      menuItemClasses: [
        // add class names to this list
        'custom-menu-item'
      ],
      // css classes that context menu will have
      contextMenuClasses: [
        // add class names to this list
        'custom-context-menu'
      ],
      // Indicates that the menu item has a submenu. If not provided default one will be used
      submenuIndicator: {src: 'assets/submenu-indicator-default.svg', width: 12, height: 12}
    });
    setTimeout(function () {
      //if(layout) layout.stop()
      layout = makeLayout();
      layout.run();
    }, 333)
  } catch (ex) {
    alert(ex)
  }
}
export default {
  name: "ui_test",
  data: () => gData,
  async mounted() {
    await init_cy(null);
  },
  methods: {
    toggleStyle() {
      alert('TODO toggleStyle')
    },
    changeEdgeLength(e) {
      layout_params.edgeLength = e;
      if (layout) layout.stop()
      layout = makeLayout();
      layout.run();
    },
    changeNodeSpacing(v) {
      //alert(v)
      layout_params.nodeSpacing = v;
      //layout_params.padding = v;
      //alert(v)
      if (layout) layout.stop()
      layout = makeLayout();
      layout.run();
    },
    //绑定搜索
    on_go() {
      let get_a = () => ({"报关单号": gData.cdn});
      //利用jQuery请求数据并调用init_cy函数
      $.get('/graph', function(result) {
        try{
          //根据数据初始化知识图谱
          init_cy(result);
        }catch (e){
          alert('error in get graph data');
        }
      }, 'json');
      //将数据转化为json格式
      // json_api(tableau_root + ':5000/neo4j.post_graph', o2s(get_a()), 'POST',
      //   (o, s) => {
      //     if (!o) return alert(s)
      //     //gData.raw = s;
      //     //cy.elements = o;
      //     console.log(o);
      //     init_cy(o);
      //     //console.log(cy.elements);
      //   })
    },
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
