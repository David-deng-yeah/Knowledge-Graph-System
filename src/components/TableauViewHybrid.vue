<template>
  <div>
    <div>
      <el-input v-model="sql" placeholder="请输入SQL语句" class="input-with-select">
        <el-select v-model="database" slot="prepend" style="width: 100px">
          <el-option
            v-for="item in selections"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <el-button slot="append" @click="sql_query" type="primary" plain>查询</el-button>
      </el-input>
      <br>
      <el-collapse v-model="activeNames">
        <el-collapse-item title="查询结果" name="1">
          <el-table :data="tableData.slice((currentPage-1)*pageSize, currentPage*pageSize)" @select="select_row"
                    @select-all="select_row" border style="width: 100%">
            <el-table-column type="selection">
            </el-table-column>
            <el-table-column v-for="key in tableKeys" v-bind:label="key">
              <template slot-scope="scope">
                {{ scope.row[key] }}
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="pageSize"
            background
            layout="total, sizes, prev, pager, next, jumper"
            :total="currentTotal">
          </el-pagination>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div style="float: right">
      <el-button type="primary" @click="handleReload">刷新</el-button>
      <el-button type="primary" @click="filterSingleValue">查询</el-button>
      <el-button type="primary" @click="removeValuesFromFilter">清空</el-button>
      <el-button type="danger" @click="dialogFormVisible = true">保存</el-button>
      <el-dialog title="路由信息" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="srt" :label-width="formLabelWidth">
            <el-input v-model="form.srt"></el-input>
          </el-form-item>
          <el-form-item label="self_key" :label-width="formLabelWidth">
            <el-input v-model="form.self_key"></el-input>
          </el-form-item>
          <el-form-item label="parent_key" :label-width="formLabelWidth">
            <el-input v-model="form.parent_key"></el-input>
          </el-form-item>
          <el-form-item label="path" :label-width="formLabelWidth">
            <el-input v-model="form.path"></el-input>
          </el-form-item>
          <el-form-item label="component" :label-width="formLabelWidth">
            <el-select v-model="form.component">
              <el-option label="TableauView" value="TableauView"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="title" :label-width="formLabelWidth">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="save">确定</el-button>
          <el-button @click="dialogFormVisible = false">取消</el-button>
        </div>
      </el-dialog>
    </div>
    <div>
      <el-input v-model="tableau_url" placeholder="请输入url">
        <el-button slot="append" @click="search_tableau_view" type="primary" plain>查询</el-button>
      </el-input>
    </div>
    <div id="vizContainer" style="height: 800px"></div>
  </div>
</template>

<script>

  import axios from "axios";

  export default {
    name: "nat_dev",
    data() {
      return {
        selections: [{
          value: 'mysql',
          label: 'mysql'
        }, {
          value: 'gbase',
          label: 'gbase'
        }],
        database: 'mysql',
        form: {
          srt: '',
          self_key: '',
          parent_key: '',
          path: '',
          component: '',
          title: '',
          url: ''
        },
        dialogFormVisible: false,
        formLabelWidth: '120px',
        containerDiv: null,
        viz: null,
        tableau_url: '/views/tableau/tableau?:showAppBanner=false&:display_count=n&:showVizHome=n&:origin=viz_share_link',
        my_url: '',
        view_url: 'about:blank',
        options: null,
        workbook: null,
        activeSheet: null,
        sql: 'select 进出境时间,进出口标记,出入境口岸,是否查验,经营单位名称 from database_1.bgds_inspection_details_2019_2020ne limit 10;',
        activeNames: ['1'],
        tableKeys: [],
        tableData: [],
        filterParameter: [],
        multipleSelection: [],
        tmp: [],
        currentPage: 1,
        pageSize: 10,
        currentTotal: 0,
        configRouter: {}
      }
    },
    inject: ['reload'],
    methods: {
      async initViz() {
        this.containerDiv = document.getElementById("vizContainer");
        // let _url = this.$route.meta.url;
        // let end = _url.indexOf("?");
        // let content_url = _url.substring(7, end);
        let end = this.tableau_url.indexOf("?");
        let content_url = this.tableau_url.substring(7, end);
        let username = sessionStorage.getItem('tableau_backend_username');
        let auth = await (await fetch('http://10.94.81.132:5000/logic.check_view?username=' + username + '&content_url=' + content_url)).json();
        if (auth.view) {
          let user_id = sessionStorage.getItem('tableau_backend_userid');
          let token_o = await (await fetch('http://10.94.81.132:5000/get_token?userid=' + user_id)).json();
          if (token_o) {
            // this.my_url = `${token_o.url}/trusted/${token_o.token}${_url}`;
            this.my_url = `${token_o.url}/trusted/${token_o.token}${this.tableau_url}`;
            this.view_url = this.my_url
            this.options = {
              hideTabs: true,
              // hideToolbar: true,
              onFirstInteractive: () => {
                this.workbook = this.viz.getWorkbook();
                this.activeSheet = this.workbook.getActiveSheet();
                console.log("Run this code when the viz has finished loading.")
              }
            };
            this.viz = new tableau.Viz(this.containerDiv, this.view_url, this.options);
          } else {
            //TODO sess expired?
          }
        } else {
          //TODO authority
          this.view_url = 'http://10.94.81.132:8080/403';
          this.options = {
            width: this.containerDiv.offsetWidth,
            height: this.containerDiv.offsetHeight,
            hideTabs: true, onFirstInteractive: () => {
              console.log("Run this code when the viz has finished loading.")
            }
          };
          this.viz = new tableau.Viz(this.containerDiv, this.view_url, this.options);
        }
      },
      async sql_query() {
        let data = {_dba: this.database, sql_sentence: this.sql}
        let rst = await fetch('http://10.94.81.132:5000/logic.sql_select_column', {
          method: 'POST',
          body: JSON.stringify(data)
        });
        let sql_table = await rst.json();
        this.tableData = sql_table['sql_data'];
        this.tableKeys = sql_table['col_array'];
      },
      handleSizeChange(val) {
        this.pageSize = val;
      },
      handleCurrentChange(val) {
        this.currentPage = val;
      },
      select_row(row) {
        this.multipleSelection = row;
      },
      filterSingleValue() {
        //TODO filterSingleValue
        // for (let i=0; i<this.multipleSelection.length; i++) {
        //   this.tmp.push(this.multipleSelection[i][this.tableKeys[4]]);
        // }
        // this.activeSheet.applyFilterAsync(
        //   this.tableKeys[4],
        //   this.tmp,
        //   tableau.FilterUpdateType.REPLACE
        // );
        // this.tmp = [];

        //TODO filterMultipleValues
        let tmp_a = [];
        for (let i = 0; i < this.multipleSelection.length; i++) {
          tmp_a[i] = [];
          for (let j = 0; j < this.filterParameter.length; j++) {
            tmp_a[i].push(this.multipleSelection[i][this.filterParameter[j]]);
          }
        }
        console.log(tmp_a);
        //transposed matrix
        let tmp_a_t = [];
        for (let i = 0; i < this.filterParameter.length; i++) {
          tmp_a_t[i] = [];
        }
        for (let i = 0; i < tmp_a.length; i++) {
          for (let j = 0; j < tmp_a[i].length; j++) {
            tmp_a_t[j][i] = tmp_a[i][j];
          }
        }
        console.log(tmp_a_t);
        this.tmp = tmp_a_t;
        //TODO filter Date Range
        // console.log(new Date(Date.now()));
        // console.log(new Date(this.tmp[0]).format('Y-m-d H:i:s').replace(/-0/g, '-'));
        // TODO TIME
        // this.activeSheet.applyRangeFilterAsync(
        //   this.tableKeys[0],
        //   {
        //     min: new Date(this.tmp[0]).format('Y-m-d H:i:s'),
        //     max: new Date(Date.now())
        //     // max: new Date(this.tmp[0]).format('Y-m-d H:i:s')
        //   },
        // );
        // this.activeSheet.applyFilterAsync(
        //   this.tableKeys[0],
        //   new Date(this.tmp[0]).format('Y-m-d H:i:s').replace(/-0/g, '/'),
        //   tableau.FilterUpdateType.REPLACE
        // );
        for (let i = 0; i < this.filterParameter.length; i++) {
          this.activeSheet.applyFilterAsync(
            this.filterParameter[i],
            this.tmp[i],
            tableau.FilterUpdateType.REPLACE
          );
        }
      },
      removeValuesFromFilter() {
        for (let i = 0; i < this.filterParameter.length; i++) {
          this.activeSheet.applyFilterAsync(
            this.filterParameter[i],
            this.tmp[i],
            tableau.FilterUpdateType.REMOVE
          );
        }
      },
      handleReload() {
        this.reload();
      },
      async save() {
        this.dialogFormVisible = false;
        this.$confirm('是否确定提交？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '提交成功！'
          });
          this.form.url = this.tableau_url.substring(19);
          this.configRouter = {
            "srt": this.form.srt,
            "self_key": this.form.self_key,
            "parent_key": this.form.parent_key,
            "path": this.form.path,
            "component": this.form.component,
            "title": this.form.title,
            "url": this.form.url,
            "db": this.database,
            "sql_sentence": this.sql
          }
          console.log(this.configRouter);
          let _post_s = o2s(this.configRouter);
          console.log(_post_s);
          let rst = axios.post('http://10.94.81.132:5000/logic.routers_insert', _post_s)
          let rst_data = rst.data || rst;
          console.log('=>', rst_data);
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消提交'
          });
        });
      },
      search_tableau_view() {
        this.initViz();
      }
    },
    mounted() {
      this.sql_query();
    },
  }
</script>

<style scoped>

</style>
