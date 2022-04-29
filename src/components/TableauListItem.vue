<template>
<div class='elem'>
	<el-button @click='showMenu' class='' :title='this.title' ref="button">
		<img :src='this.img_path' v-if="this.img_path!=null" />
		<h3 class='title'>{{itemdata.name}}</h3>
		<span class='description' v-if="this.img_path==null">{{this.project_content}}</span><br />
		<span class='description'>{{itemdata.description}}</span>
	</el-button>
</div>
</template>
<script>
export default{
	name:"TableauListItem",
	data(){
		return{
				// :disabled="dontShowPop"
			dontShowPop: true
		}
	},
	props:{
		itemdata:{
			type:Object,
			default:{
				id:'',
				created_at:'',
				updated_at:'',
				img_path:'',
				name:'',
				description:''
			}
		},
		baseurl:{
			type:String,
			default:''
		}
	},
	computed:{
		title(){
			return "created at: "+this.itemdata.created_at+"\nupdated_at: "+this.itemdata.updated_at
		},
		img_path(){
			var img_path = this.itemdata.img_path
			if (img_path==null)
				return null;
			else
				return this.baseurl+img_path;
		},
		project_content(){
			var children = this.itemdata.children
			var num = (children!=null)?children.length:0
			if (num<=1)
				return "(Has "+num+" workbook)."
			else
				return "(Has "+num+" workbooks)."
		}
	},
	methods:{
		showMenu(event){
			/*if (event.button==0){
				this.dontShowPop=false
			}
			cosole.log(event.button)*/
			this.$emit("menu", this.itemdata, this.$refs["button"].$el)
		}
	}
}
</script>
<style scoped>
.elem{
	margin:20px;flex:1;
	text-align:center;
	max-width:200px;
	min-width:200px;
	background: white;
}

/*
.elem h3:hover{
	text-decoration:underline;
}
*/

.elem img{
	width:100%;
}

.elem .title{
	word-break:break-all;
	word-wrap:break-word;
	white-space:normal;
}

.elem .description{
	word-break:break-all;
	word-wrap:break-word;
	white-space:normal;
}

.menu-class{
    width: 100%;
}
.el-menu-item{
	font-size:16px;
	height:32px;
	line-height:32px;
	padding:0 !important;
}
</style>
