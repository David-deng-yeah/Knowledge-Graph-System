<template>
  <div>
    <el-time-picker
      is-range
      v-model="value1"
      range-seperator="-"
      start-placeholder="开始时间"
      end-placeholder="结束时间"
      placeholder="选择时间范围">
    </el-time-picker>
    <el-time-select
      placeholder="起始时间"
      v-model="startTime"
      picker-options="{
        start: '08:30',
        step: '00:15',
        end: '18:30'
      }">
    </el-time-select>
    <el-time-select
      placeholder="结束时间"
      v-model="endTime"
      picker-options="{
        start: '8:30',
        step: '00:15',
        end: '18:30',
        minTime: startTime
      }">
    </el-time-select>
  </div>
</template>

<script>
  export default {
    name: "Message",
    data() {
      return {
        value1: [new Date(), new Date()],
        startTime: '',
        endTime: ''
      }
    }
  }
</script>

<style scoped>

</style>
