import Vue from 'vue'
import App from './App.vue'
import router from '../../VueProject/offline-map-master/src/router'

import 'element-ui/lib/theme-chalk/index.css'; //浅蓝色主题
import ElementUI from 'element-ui';
import "./assets/main.css"
import "./assets/dark-theme.css"

import jquery from 'jquery'
import './directives/dialogDrag.js';

Vue.use(ElementUI, {
  size: 'small'
});

Vue.prototype.jq = jquery

let gVue;

// async function get_menu_json_and_insert() {
//   try {
//     let m_a = await fetch('http://10.94.81.132:5000/logic.get_routers')
//       .then(response => {
//         return response.json()
//       })
//       .catch(err => {
//         console.log(err);
//       })
//     //TODO copy o2s/s2o() here
//     sessionStorage.setItem('tableau_menu_a', o2s(m_a));
//     //TODO fetch json
//     let d_routes = [];
//     for (let m in m_a.router) {
//       let _item;
//       let v = m_a.router[m] || {};
//       if (v.children) {
//         let _c = [];
//         for (let c in v.children) {
//           _c.push({
//             path: v.children[c].path,
//             component: () => import('../src/components/' + v.children[c].component),
//             meta: {
//               id: v.children[c].meta.id,
//               srt: v.children[c].meta.srt,
//               self_key: v.children[c].meta.self_key,
//               parent_key: v.children[c].meta.parent_key,
//               title: v.children[c].meta.title,
//               url: v.children[c].meta.url,
//               db: v.children[c].meta.db,
//               sql_sentence: v.children[c].meta.sql_sentence
//             }
//           })
//         }
//         _item = {
//           path: v.path,
//           component: () => import('../src/components/' + v.component),
//           meta: {
//             id: v.meta.id,
//             srt: v.meta.srt,
//             self_key: v.meta.self_key,
//             parent_key: v.meta.parent_key,
//             title: v.meta.title,
//             url: v.meta.url,
//             db: v.meta.db,
//             sql_sentence: v.meta.sql_sentence
//           },
//           children: _c
//         }
//       } else {
//         let _c = [{
//           path: v.path,
//           component: () => import('../src/components/' + v.component),
//           meta: {
//             id: v.meta.id,
//             srt: v.meta.srt,
//             self_key: v.meta.self_key,
//             parent_key: v.meta.parent_key,
//             title: v.meta.title,
//             url: v.meta.url,
//             db: v.meta.db,
//             sql_sentence: v.meta.sql_sentence
//           }
//         }];
//         _item = {
//           path: '/',
//           component: () => import('../src/components/' + 'Home.vue'),
//           meta: {
//             id: v.meta.id,
//             srt: v.meta.srt,
//             self_Key: v.meta.self_key,
//             parent_key: v.meta.parent_key,
//             title: v.meta.title,
//             url: v.meta.url,
//             db: v.meta.db,
//             sql_sentence: v.meta.sql_sentence
//           },
//           children: _c,
//         };
//       }
//       if (_item)
//         d_routes.push(_item);
//     }
//     router.addRoutes(d_routes)
//   } catch (ex) {
//     alert(ex)
//   }
// }
//
// setTimeout(get_menu_json_and_insert, 11);

/* main.js will be inserted into the generated html.
This is a way to use the 'app' component only once*/
gVue = new Vue({
  el: '#app',
  render: h => h(App),
  router: router
})
