<template>
  <div>
    <div>
      <el-row>
        <el-input v-model="bgd" placeholder="请输入报关单号">
          <el-button
            slot="append"
            @click="bgd_query"
            type="primary"
            plain>
            查询
          </el-button>
        </el-input>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">报关单主要信息</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">报关单号: {{报关单号}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">进出境时间: {{进出境时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">出入境口岸: {{出入境口岸}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">申报时间: {{申报时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">申报口岸: {{申报口岸}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">申报毛重: {{申报毛重}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">申报净重: {{申报净重}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">确报时间: {{确报时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">贸易方式: {{贸易方式}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">运输方式: {{运输方式}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">是否删单: {{是否删单}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">排班日期: {{排班日期}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">班次: {{班次}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple"></div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">申报单位代码: {{申报单位代码}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">申报单位名称: {{申报单位名称}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">申报单位法人: {{申报单位法人}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">申报单位法人证件号: {{申报单位法人证件号}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">经营单位代码: {{经营单位代码}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">经营单位名称: {{经营单位名称}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">经营单位法人: {{经营单位法人}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">经营单位法人证件号: {{经营单位法人证件号}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">货主单位代码: {{货主单位代码}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">货主单位名称: {{货主单位名称}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">货主单位法人: {{货主单位法人}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">货主单位法人证件号: {{货主单位法人证件号}}</div>
        </el-col>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">报关单备注: {{报关单备注}}</div>
      </el-row>
    </div>
    <div>
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">申报货物信息</div>
        </el-col>
      </el-row>
      <el-table :data="cargoInformation" border style="width: 100%">
        <el-table-column v-for="key in cargoInformationKeys" v-bind:label="key">
          <template slot-scope="scope">
            {{ scope.row[key] }}
          </template>
        </el-table-column>
      </el-table>
      <el-col :span="24">
        <div class="grid-content bg-purple-light">美元申报总值: {{美元申报总值}}</div>
      </el-col>
    </div>
    <div>
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">舱单信息</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">舱单号: {{舱单号}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">是否空车: {{是否空车}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">运输工具ID: {{运输工具ID}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">车牌号: {{车牌号}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">司机ID: {{司机ID}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">司机姓名: {{司机姓名}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">车辆拥有人: {{车辆拥有人}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">运输行名称: {{运输行名称}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">车辆类型: {{车辆类型}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">提运单号: {{提运单号}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">舱单删单标记: {{舱单删单标记}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">舱单绑定类型: {{舱单绑定类型}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">车辆重量: {{车辆重量}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">货物重量: {{货物重量}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">称重: {{称重}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">真实毛重: {{真实毛重}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">生鲜标记: {{生鲜标记}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">卡口单证类型: {{卡口单证类型}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">卡口派位信息: {{卡口派位信息}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">停靠区域: {{停靠区域}}</div>
        </el-col>
      </el-row>
    </div>
    <div v-if="是否机检 === '是'">
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">机检信息</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">是否机检: {{是否机检}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">查验任务单号: {{查验任务单号}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple"></div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">机检班次: {{机检班次}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">机检科室: {{机检科室}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">机检科长: {{机检科长}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">布控时间: {{布控时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">布控科室: {{布控科室}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">布控人代码: {{布控人代码}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">布控人工备注: {{布控人工备注}}</div>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">机检人A: {{机检人A}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">机检人B: {{机检人B}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">机检时间A: {{机检时间A}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">机检时间B: {{机检时间B}}</div>
        </el-col>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">机检内容: {{机检内容}}</div>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">机检结果: {{机检结果}}</div>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">机检结果详情: {{机检结果详情}}</div>
      </el-row>
    </div>
    <div v-if="是否查验 === '是'">
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple-dark">人工查验信息</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">是否查验: {{是否查验}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">中控时间: {{中控时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">派单时间: {{派单时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">中控到派单时间: {{中控到派单时间}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">查验科室: {{查验科室}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">查验科长: {{查验科长}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">当班科室: {{当班科室}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">下一当班科室: {{下一当班科室}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">记录单创建时间: {{记录单创建时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">查验开始时间: {{查验开始时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">查验结束时间: {{查验结束时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">派单到结束时间: {{派单到结束时间}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">主查人员: {{主查人员}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">辅查人员: {{辅查人员}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">查验台位: {{查验台位}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">查验方式: {{查验方式}}</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">是否异常: {{是否异常}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">查获类型: {{查获类型}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">科长审批时间: {{科长审批时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">人工查验口岸状态: {{人工查验口岸状态}}</div>
        </el-col>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">人工查验记录: {{人工查验记录}}</div>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">人工查验结果: {{人工查验结果}}</div>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">人工查验处理结果: {{人工查验处理结果}}</div>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">人工查验处理意见: {{人工查验处理意见}}</div>
      </el-row>
      <el-row :span="24">
        <div class="grid-content bg-purple" type="textarea">指令要求: {{指令要求}}</div>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">首次派单时间: {{首次派单时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">首次派单时间: {{首次派单时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">首次派单科室: {{首次派单科室}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">首次派单主查: {{首次派单主查}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">首次派单辅查: {{首次派单辅查}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">是否改派单: {{是否改派单}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">派单人工干预标志: {{派单人工干预标志}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">派单人工干预描述: {{派单人工干预描述}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple"></div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">审单员: {{审单员}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">审核内容: {{审核内容}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">审单日期: {{审单日期}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <div class="grid-content bg-purple">处置结束时间: {{处置结束时间}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">处置部门: {{处置部门}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">处置人: {{处置人}}</div>
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple-light">处置结果: {{处置结果}}</div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  let sql_table;
  let data;
  let cargo_information_table;

  export default {
    name: "CustomsDeclarationearch",
    data() {
      return {
        bgd: '',
        报关单号: '',
        进出境时间: '',
        出入境口岸: '',
        申报时间: '',
        申报口岸: '',
        申报毛重: '',
        申报净重: '',
        确报时间: '',
        贸易方式: '',
        运输方式: '',
        是否删单: '',
        排班日期: '',
        班次: '',
        申报单位代码: '',
        申报单位名称: '',
        申报单位法人: '',
        申报单位法人证件号: '',
        经营单位代码: '',
        经营单位名称: '',
        经营单位法人: '',
        经营单位法人证件号: '',
        货主单位代码: '',
        货主单位名称: '',
        货主单位法人: '',
        货主单位法人证件号: '',
        报关单备注: '',
        美元申报总值: '',
        舱单号: '',
        是否空车: '',
        运输工具ID: '',
        车牌号: '',
        司机ID: '',
        司机姓名: '',
        车辆拥有人: '',
        运输行名称: '',
        车辆类型: '',
        提运单号: '',
        舱单删单标记: '',
        舱单绑定类型: '',
        车辆重量: '',
        货物重量: '',
        称重: '',
        真实毛重: '',
        生鲜标记: '',
        卡口单证类型: '',
        卡口派位信息: '',
        停靠区域: '',
        是否机检: '',
        查验任务单号: '',
        机检班次: '',
        机检科室: '',
        机检科长: '',
        布控时间: '',
        布控科室: '',
        布控人代码: '',
        布控人工备注: '',
        机检人A: '',
        机检人B: '',
        机检时间A: '',
        机检时间B: '',
        机检内容: '',
        机检结果: '',
        机检结果详情: '',
        是否查验: '',
        中控时间: '',
        派单时间: '',
        中控到派单时间: '',
        查验科室: '',
        查验科长: '',
        当班科室: '',
        下一当班科室: '',
        记录单创建时间: '',
        查验开始时间: '',
        查验结束时间: '',
        派单到结束时间: '',
        主查人员: '',
        辅查人员: '',
        查验台位: '',
        查验方式: '',
        是否异常: '',
        查获类型: '',
        科长审批时间: '',
        人工查验口岸状态: '',
        人工查验记录: '',
        人工查验结果: '',
        人工查验处理结果: '',
        人工查验处理意见: '',
        指令要求: '',
        首次派单时间: '',
        首次派单科长: '',
        首次派单科室: '',
        首次派单主查: '',
        首次派单辅查: '',
        是否改派单: '',
        派单人工干预标志: '',
        派单人工干预描述: '',
        审单员: '',
        审核内容: '',
        审单日期: '',
        处置结束时间: '',
        处置部门: '',
        处置人: '',
        处置结果: '',
        tableKeys: [],
        tableData: [],
        cargoInformationKeys: [],
        cargoInformation: []
      }
    },
    methods: {
      async bgd_query() {
        data = {报关单号: this.bgd}
        let rst = await fetch('http://10.94.81.132:5000/logic.bgd_search', {
          method: 'POST',
          body: JSON.stringify(data)
        });
        sql_table = await rst.json();

        let cargo_rst = await fetch('http://10.94.81.132:5000/logic.bgd_search_cargo_information', {
          method: 'POST',
          body: JSON.stringify(data)
        });
        cargo_information_table = await cargo_rst.json();

        await this.bgd_init();
      },
      async bgd_init() {
        if (sql_table) {
          localStorage.setItem('last_bgd_query', o2s(sql_table));
        }
        sql_table = s2o(localStorage.getItem('last_bgd_query'))
        this.tableData = sql_table['sql_data'];
        this.tableKeys = sql_table['col_array'];
        this.报关单号 = this.tableData[0].报关单号;
        this.进出境时间 = this.tableData[0].进出境时间;
        this.出入境口岸 = this.tableData[0].出入境口岸;
        this.申报时间 = this.tableData[0].申报时间;
        this.申报口岸 = this.tableData[0].申报口岸;
        this.申报毛重 = this.tableData[0].申报毛重;
        this.申报净重 = this.tableData[0].申报净重;
        this.确报时间 = this.tableData[0].确报时间;
        this.贸易方式 = this.tableData[0].贸易方式;
        this.运输方式 = this.tableData[0].运输方式;
        this.是否删单 = this.tableData[0].是否删单;
        this.排班日期 = this.tableData[0].排班日期;
        this.班次 = this.tableData[0].班次;
        this.申报单位代码 = this.tableData[0].申报单位代码;
        this.申报单位名称 = this.tableData[0].申报单位名称;
        this.申报单位法人 = this.tableData[0].申报单位法人;
        this.申报单位法人证件号 = this.tableData[0].申报单位法人证件号;
        this.经营单位代码 = this.tableData[0].经营单位代码;
        this.经营单位名称 = this.tableData[0].经营单位名称;
        this.经营单位法人 = this.tableData[0].经营单位法人;
        this.经营单位法人证件号 = this.tableData[0].经营单位法人证件号;
        this.货主单位代码 = this.tableData[0].货主单位代码;
        this.货主单位名称 = this.tableData[0].货主单位名称;
        this.货主单位法人 = this.tableData[0].货主单位法人;
        this.货主单位法人证件号 = this.tableData[0].货主单位法人证件号;
        this.报关单备注 = this.tableData[0].报关单备注;
        this.美元申报总值 = this.tableData[0].美元申报总值;
        this.舱单号 = this.tableData[0].舱单号;
        this.是否空车 = this.tableData[0].是否空车;
        this.运输工具ID = this.tableData[0].运输工具ID;
        this.车牌号 = this.tableData[0].车牌号;
        this.司机ID = this.tableData[0].司机ID;
        this.司机姓名 = this.tableData[0].司机姓名;
        this.车辆拥有人 = this.tableData[0].车辆拥有人;
        this.运输行名称 = this.tableData[0].运输行名称;
        this.车辆类型 = this.tableData[0].车辆类型;
        this.提运单号 = this.tableData[0].提运单号;
        this.舱单删单标记 = this.tableData[0].舱单删单标记;
        this.舱单绑定类型 = this.tableData[0].舱单绑定类型;
        this.车辆重量 = this.tableData[0].车辆重量;
        this.货物重量 = this.tableData[0].货物重量;
        this.称重 = this.tableData[0].称重;
        this.真实毛重 = this.tableData[0].真实毛重;
        this.生鲜标记 = this.tableData[0].生鲜标记;
        this.卡口单证类型 = this.tableData[0].卡口单证类型;
        this.卡口派位信息 = this.tableData[0].卡口派位信息;
        this.停靠区域 = this.tableData[0].停靠区域;
        this.是否机检 = this.tableData[0].是否机检;
        this.查验任务单号 = this.tableData[0].查验任务单号;
        this.机检班次 = this.tableData[0].机检班次;
        this.机检科室 = this.tableData[0].机检科室;
        this.机检科长 = this.tableData[0].机检科长;
        this.布控时间 = this.tableData[0].布控时间;
        this.布控科室 = this.tableData[0].布控科室;
        this.布控人代码 = this.tableData[0].布控人代码;
        this.布控人工备注 = this.tableData[0].布控人工备注;
        this.机检人A = this.tableData[0].机检人A;
        this.机检人B = this.tableData[0].机检人B;
        this.机检时间A = this.tableData[0].机检时间A;
        this.机检时间B = this.tableData[0].机检时间B;
        this.机检内容 = this.tableData[0].机检内容;
        this.机检结果 = this.tableData[0].机检结果;
        this.机检结果详情 = this.tableData[0].机检结果详情;
        this.是否查验 = this.tableData[0].是否查验;
        this.中控时间 = this.tableData[0].中控时间;
        this.派单时间 = this.tableData[0].派单时间;
        this.中控到派单时间 = this.tableData[0].中控到派单时间;
        this.查验科室 = this.tableData[0].查验科室;
        this.查验科长 = this.tableData[0].查验科长;
        this.当班科室 = this.tableData[0].当班科室;
        this.下一当班科室 = this.tableData[0].下一当班科室;
        this.记录单创建时间 = this.tableData[0].记录单创建时间;
        this.查验开始时间 = this.tableData[0].查验开始时间;
        this.查验结束时间 = this.tableData[0].查验结束时间;
        this.派单到结束时间 = this.tableData[0].派单到结束时间;
        this.主查人员 = this.tableData[0].主查人员;
        this.辅查人员 = this.tableData[0].辅查人员;
        this.查验台位 = this.tableData[0].查验台位;
        this.查验方式 = this.tableData[0].查验方式;
        this.是否异常 = this.tableData[0].是否异常;
        this.查获类型 = this.tableData[0].查获类型;
        this.科长审批时间 = this.tableData[0].科长审批时间;
        this.人工查验口岸状态 = this.tableData[0].人工查验口岸状态;
        this.人工查验记录 = this.tableData[0].人工查验记录;
        this.人工查验结果 = this.tableData[0].人工查验结果;
        this.人工查验处理结果 = this.tableData[0].人工查验处理结果;
        this.人工查验处理意见 = this.tableData[0].人工查验处理意见;
        this.指令要求 = this.tableData[0].指令要求;
        this.首次派单时间 = this.tableData[0].首次派单时间;
        this.首次派单科长 = this.tableData[0].首次派单科长;
        this.首次派单科室 = this.tableData[0].首次派单科室;
        this.首次派单主查 = this.tableData[0].首次派单主查;
        this.首次派单辅查 = this.tableData[0].首次派单辅查;
        this.是否改派单 = this.tableData[0].是否改派单;
        this.派单人工干预标志 = this.tableData[0].派单人工干预标志;
        this.派单人工干预描述 = this.tableData[0].派单人工干预描述;
        this.审单员 = this.tableData[0].审单员;
        this.审核内容 = this.tableData[0].审核内容;
        this.审单日期 = this.tableData[0].审单日期;
        this.处置结束时间 = this.tableData[0].处置结束时间;
        this.处置部门 = this.tableData[0].处置部门;
        this.处置人 = this.tableData[0].处置人;
        this.处置结果 = this.tableData[0].处置结果;

        if (cargo_information_table) {
          localStorage.setItem('last_cargo_information_search', o2s(cargo_information_table));
        }
        cargo_information_table = s2o(localStorage.getItem('last_cargo_information_search'));
        this.cargoInformation = cargo_information_table['sql_data'];
        this.cargoInformationKeys = cargo_information_table['col_array'];
      }
    },
    mounted() {
      this.bgd_init();
    }
  }
</script>

<style scoped>
  .el-row {
    margin-bottom: 20px;
  }

  .el-col {
    border-radius: 4px;
  }

  .bg-purple-dark {
    background: #99a9bf;
  }

  .bg-purple {
    background: #d3dce6;
  }

  .bg-purple-light {
    background: #e5e9f2;
  }

  .grid-content {
    border-radius: 4px;
    height: 36px;
    line-height: 36px;
    text-indent: 10px;
  }

  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
