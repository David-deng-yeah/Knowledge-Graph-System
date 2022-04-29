<template>
  <div>
    <div>
      <el-collapse v-model="activeNames">
        <el-collapse-item title="查询结果" name="1">
<!--          <el-table :data="tableKeys" @select="select_filter_parameters" @select-all="select_filter_parameters" border-->
<!--                    style="width: 100%">-->
<!--            <el-table-column type="selection" width="50px">-->
<!--            </el-table-column>-->
<!--            <el-table-column>-->
<!--              <template slot-scope="scope">-->
<!--                {{ scope.row }}-->
<!--              </template>-->
<!--            </el-table-column>-->
<!--          </el-table>-->
<!--          <br>-->
          <el-table :data="tableData.slice((currentPage-1)*pageSize, currentPage*pageSize)" border style="width: 100%">
<!--            <el-table-column type="selection">-->
<!--            </el-table-column>-->
            <el-table-column width="50px">
<!--              <template slot="header" slot-scope="scope">-->
<!--                <el-checkbox v-model="checkboxPageList[currentPage-1]" @change="select_all_rows"></el-checkbox>-->
<!--              </template>-->
              <template slot-scope="scope">
                <el-checkbox v-model="checkboxRowList[scope.$index+(currentPage-1)*pageSize]" @change="select_rows">
                </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column v-for="(key, index) in tableKeys" v-bind:label="key">
              <template slot="header" slot-scope="scope">
                <el-checkbox v-model="checkboxList[index]" @change="select_filter_parameters">
                  {{ key }}
                </el-checkbox>
              </template>
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
      <el-button type="primary" @click="filterSingleValue">查询</el-button>
      <el-button type="primary" @click="removeValuesFromFilter">清空</el-button>
      <el-button type="danger" @click="dialogFormVisible = true" v-show="isShow">修改</el-button>
      <el-dialog title="路由信息" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="url" :label-width="formLabelWidth">
            <el-input v-model="form.url"></el-input>
          </el-form-item>
          <el-form-item label="db" :label-width="formLabelWidth">
            <el-select v-model="form.db">
              <el-option label="mysql" value="mysql"></el-option>
              <el-option label="gbase" value="gbase"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="sql" :label-width="formLabelWidth">
            <el-input v-model="form.sql"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="handleUpdate">确定</el-button>
          <el-button @click="dialogFormVisible = false">取消</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="vizContainer" style="height: 800px"></div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "TableauView",
    data() {
      return {
        database: '',
        form: {
          url: this.$route.meta.url,
          db: this.$route.meta.db,
          sql: this.$route.meta.sql_sentence
        },
        dialogFormVisible: false,
        formLabelWidth: '120px',
        isShow: false,
        containerDiv: null,
        viz: null,
        my_url: '',
        view_url: 'about:blank',
        options: null,
        workbook: null,
        activeSheet: null,
        sql: '',
        activeNames: ['1'],
        tableKeys: [],
        tableData: [],
        checkboxList: [],
        // checkboxPageList: [],
        checkboxRowList: [],
        filterParameter: [],
        multipleSelection: [],
        tmp: [],
        currentPage: 1,
        pageSize: 10,
        currentTotal: 0
      }
    },
    methods: {
      async initViz() {
        this.containerDiv = document.getElementById("vizContainer");
        let _url = this.$route.meta.url;
        let end = _url.indexOf("?");
        let content_url = _url.substring(7, end);
        let username = sessionStorage.getItem('tableau_backend_username');
        let auth = await (await fetch('http://10.94.81.132:5000/logic.check_view?username=' + username + '&content_url=' + content_url)).json();
        if (auth.view) {
          let user_id = sessionStorage.getItem('tableau_backend_userid');
          let token_o = await (await fetch('http://10.94.81.132:5000/get_token?userid=' + user_id)).json();
          if (token_o) {
            this.my_url = `${token_o.url}/trusted/${token_o.token}${_url}`;
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
        this.database = this.$route.meta.db;
        this.sql = this.$route.meta.sql_sentence;
        let data = {_dba: this.database, sql_sentence: this.sql}
        let rst = await fetch('http://10.94.81.132:5000/logic.sql_select_column', {
          method: 'POST',
          body: JSON.stringify(data)
        });
        let sql_table = await rst.json();
        this.tableData = sql_table['sql_data'];
        //TODO Select All
        // for (let i=0; i<this.tableData.length/this.pageSize; i++) {
        //   this.checkboxPageList[i] = false;
        // }
        for (let i=0; i<this.tableData.length; i++) {
          this.checkboxRowList[i] = false;
        }
        this.tableKeys = sql_table['col_array'];
        this.currentTotal = this.tableData.length;
      },
      handleSizeChange(val) {
        this.pageSize = val;
      },
      handleCurrentChange(val) {
        this.currentPage = val;
      },
      // select_filter_parameters(row) {
      //   this.filterParameter = row;
      // },
      select_filter_parameters() {
        let l = [];
        for (let i=0; i<this.checkboxList.length; i++) {
          if (this.checkboxList[i] == true) {
            l.push(this.tableKeys[i]);
          }
        }
        this.filterParameter = l;
        // console.log(this.filterParameter);
      },
      select_rows() {
        let r = [];
        for (let i=0; i<this.checkboxRowList.length; i++) {
          if (this.checkboxRowList[i] == true) {
            r.push(this.tableData[i]);
          }
        }
        this.multipleSelection = r;
      },
      //TODO Select All
      // select_all_rows() {
      //   let r = [];
      //   for (let i=0; i<this.checkboxPageList.length; i++) {
      //     if (this.checkboxPageList[i] == true) {
      //       for (let j=(this.currentPage-1)*this.pageSize; j<this.currentPage*this.pageSize; j++) {
      //         this.checkboxRowList[j] = true;
      //       }
      //     }
      //   }
      //   for (let i=0; i<this.checkboxRowList.length; i++) {
      //     if (this.checkboxRowList[i] == true) {
      //       r.push(this.tableData[i]);
      //     }
      //   }
      //   this.multipleSelection = r;
      // },
      // select_row(row) {
      //   this.multipleSelection = row;
      // },
      filterSingleValue() {
        //TODO filterMultipleValues
        let tmp_a = [];
        for (let i = 0; i < this.multipleSelection.length; i++) {
          tmp_a[i] = [];
          for (let j = 0; j < this.filterParameter.length; j++) {
            tmp_a[i].push(this.multipleSelection[i][this.filterParameter[j]]);
          }
        }
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
        this.tmp = tmp_a_t;
        //TODO filter Date Range
        // this.activeSheet.applyRangeFilterAsync(
        //   this.tableKeys[0],
        //   {
        //     min: new Date(this.tmp[0]).format('Y-m-d H:i:s'),
        //     max: new Date(Date.now())
        //   },
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
      handleUpdate() {
        this.dialogFormVisible = false;
        this.$confirm('是否确定修改？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '修改成功！'
          });
          this.configRouter = {
            "id": this.$route.meta.id,
            "srt": this.$route.meta.srt,
            "self_key": this.$route.meta.self_key,
            "parent_key": this.$route.meta.parent_key,
            "path": this.$route.path,
            "component": "TableauView",
            "title": this.$route.meta.title,
            "url": this.form.url,
            "db": this.form.db,
            "sql_sentence": this.form.sql
          }
          console.log(this.configRouter);
          let _post_s = o2s(this.configRouter);
          console.log(_post_s);
          let rst = axios.post('http://10.94.81.132:5000/logic.routers_update', _post_s)
          let rst_data = rst.data || rst;
          console.log('=>', rst_data);
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消修改'
          });
        });
      }
    },
    mounted() {
      let username = sessionStorage.getItem('tableau_backend_username');
      if (username == 'kjr') this.isShow = true;
      this.initViz();
      this.sql_query();
    },
  }
</script>

<style scoped>

</style>
