<template>
  <div>
    <el-table :data="gData.tableData" border style="width: 100%">
      <el-table-column label="SRT" min-width="5%" align="center">
        <template slot-scope="scope">
          <el-input v-model="scope.row.srt" :disabled="scope.row.disable"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="SELF_KEY" min-width="10%" align="center">
        <template slot-scope="scope">
          <el-input v-model="scope.row.self_key" :disabled="scope.row.disable"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="PARENT_KEY" min-width="10%" align="center">
        <template slot-scope="scope">
          <el-input v-model="scope.row.parent_key" :disabled="scope.row.disable"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="PATH" min-width="10%" align="center">
        <template slot-scope="scope">
          <el-input v-model="scope.row.path" :disabled="scope.row.disable"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="COMPONENT" min-width="10%" align="center">
        <template slot-scope="scope">
          <el-select v-model="scope.row.component" :disabled="scope.row.disable">
            <el-option
              v-for="component in gData.components"
              :key="component.option"
              :label="component.desc"
              :value="component.name">
            </el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="TITLE" min-width="10%" align="center">
        <template slot-scope="scope">
          <el-input v-model="scope.row.title" :disabled="scope.row.disable"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="URL" min-width="10%" align="center">
        <template slot-scope="scope">
          <el-input v-model="scope.row.url" :disabled="scope.row.disable"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="Operation" min-width="15%" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" plain @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
          <el-button size="mini" type="primary" plain @click="handleAdd(scope.$index, scope.row)">Add</el-button>
          <el-button size="mini" type="danger" plain @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!--  增加、修改对话框 start-->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="400px" @close="closeDialog">
      <el-form ref="form" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="SRT" prop="srt">
          <el-input v-model="form.srt"></el-input>
        </el-form-item>
        <el-form-item label="SELF_KEY" prop="self_key">
          <el-input v-model="form.self_key"></el-input>
        </el-form-item>
        <el-form-item label="PARENT_KEY" prop="parent_key">
          <el-input v-model="form.parent_key"></el-input>
        </el-form-item>
        <el-form-item label="PATH" prop="path">
          <el-input v-model="form.path"></el-input>
        </el-form-item>
        <el-form-item label="COMPONENT" prop="component">
          <el-select v-model="form.component">
            <el-option
              v-for="component in gData.components"
              :key="component.option"
              :label="component.desc"
              :value="component.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="TITLE" prop="title">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="URL" prop="url">
          <el-input v-model="form.url"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="el-footer">
        <el-button @click="closeDialog">取 消</el-button>
        <el-button type="primary" @click="onSubmit">确 定</el-button>
      </span>
    </el-dialog>
    <!--  增加、修改对话框 end-->
  </div>
</template>

<script>
  import axios from "axios";

  //优化配置路由
  export default {
    name: "Edit",
    data() {
      return {
        gData: {
          tableData: null,
          // flag: false,
          components: [
            {
              option: '选项1',
              name: 'Home',
              desc: '主页'
            },
            {
              option: '选项2',
              name: 'TableauViewIframe',
              desc: 'Tableau视图'
            },
            {
              option: '选项3',
              name: 'TableauViewHybrid',
              desc: '混编测试'
            }
          ]
        },
        dialogVisible: false,
        dialogTitle: '',
        dialogIsAdd: false,
        form: {
          srt: '',
          self_key: '',
          parent_key: '',
          path: '',
          component: '',
          title: '',
          url: '',
          db: '',
          sql_sentence: '',
        },
        rules: {
          srt: [{required: true, message: '请填写SRT', trigger: 'blur'}],
          self_key: [{required: true, message: '请填写SELF_KEY', trigger: 'blur'}],
          path: [{required: true, message: '请填写PATH', trigger: 'blur'}],
          component: [{required: true, message: '请选择COMPONENT', trigger: 'change'}],
          title: [{required: true, message: '请填写TITLE', trigger: 'blur'}],
          url: [{required: true, message: '请填写URL', trigger: 'blur'}],
        },
      };
    },
    async mounted() {
      await this.getPage();
    },
    methods: {
      handleEdit(index, row) {
        this.dialogVisible = true;
        this.dialogIsAdd = false;
        this.dialogTitle = "编辑路由";
        this.form = row;
      },
      handleAdd(index, row) {
        this.dialogVisible = true;
        this.dialogIsAdd = true;
        this.dialogTitle = "新增路由";
        this.form = {
          srt: '',
          self_key: '',
          parent_key: '',
          path: '',
          component: '',
          title: '',
          url: '',
          db: '',
          sql_sentence: '',
        };
      },
      handleDelete(index, row) {
        this.$confirm('是否确定删除？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let _post_s = o2s(row);
          let rst = axios.post('http://10.94.81.132:5000/logic.routers_delete', _post_s).then(res => {
            if (res.data.type == 'ok') {
              this.$message({
                type: 'success',
                message: '删除成功！'
              });
              this.getPage();
            } else {
              this.$message({
                type: 'error',
                message: '删除失败！',
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      async getPage() {
        let rst_fetch = await fetch('http://10.94.81.132:5000/logic.routers_show');
        let m_a = await rst_fetch.json();
        this.gData.tableData = m_a;
      },
      closeDialog() {
        this.dialogVisible = false;
        this.form = {
          srt: '',
          self_key: '',
          parent_key: '',
          path: '',
          component: '',
          title: '',
          url: '',
          db: '',
          sql_sentence: '',
        };
      },
      async onSubmit() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            let _post_s = o2s(this.form);
            if (this.dialogIsAdd) {
              axios.post('http://10.94.81.132:5000/logic.routers_insert', _post_s).then(res => {
                if (res.data.type == 'ok') {
                  this.$message({
                    type: 'success',
                    message: '增加成功！'
                  });
                  this.getPage();
                } else {
                  this.$message({
                    type: 'error',
                    message: '增加失败！',
                  });
                }
              })
              this.dialogVisible = false;
            } else {
              axios.post('http://10.94.81.132:5000/logic.routers_update', _post_s).then(res => {
                if (res.data.type == 'ok') {
                  this.$message({
                    type: 'success',
                    message: '编辑成功！'
                  });
                  this.getPage();
                } else {
                  this.$message({
                    type: 'error',
                    message: '编辑失败！',
                  });
                }
              })
              this.dialogVisible = false;
            }
          } else {
            return false;
          }
        })

      },
    }
  }
</script>

<style scoped>

</style>
