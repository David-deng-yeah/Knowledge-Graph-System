<template>
  <div>
    <el-input v-model="sql" aria-placeholder="请输入SQL语句">
      <el-button slot="append" @click="sql_query" type="primary" plain>查询</el-button>
    </el-input>
    <br>
    <el-collapse v-model="activeNames">
      <el-collapse-item title="查询结果" name="1">
        <el-table :data="tableData" border style="width: 100%">
          <el-table-column type="selection">
          </el-table-column>
          <el-table-column v-for="key in tableKeys" v-bind:label="key">
            <template slot-scope="scope">
              {{ scope.row[key] }}
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
  // let gData = {
  //   sql: '',
  //   activeNames: ['1'],
  //   tableKeys: null,
  //   tableData: null
  // };

  export default {
    name: "SqlTable",
    // data() {
    //   return gData
    // },
    data() {
      return {
        sql: '',
        activeNames: ['1'],
        tableKeys: null,
        tableData: null
      }
    },
    methods: {
      // async select() {
      //   let data = {sql_sentence: gData.sql}
      //   let rst = await fetch('http://10.94.81.132:5000/logic.sql_select_column', {
      //     method: 'POST',
      //     body: JSON.stringify(data)
      //   });
      //   let sql_table = await rst.json();
      //   gData.tableData = sql_table['sql_data'];
      //   gData.tableKeys = sql_table['col_array'];
      //   console.log(gData.tableKeys[0]);
      // },
      async sql_query() {
        let data = {sql_sentence: this.sql}
        let rst = await fetch('http://10.94.81.132:5000/logic.sql_select_column', {
          method: 'POST',
          body: JSON.stringify(data)
        });
        let sql_table = await rst.json();
        this.tableData = sql_table['sql_data'];
        this.tableKeys = sql_table['col_array'];
        console.log(this.tableKeys[0]);
      },
    },
    mounted() {
      this.sql_query();
    }
  }
</script>

<style scoped>

</style>
