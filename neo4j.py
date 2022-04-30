import traceback
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import to_pydot
from matplotlib.font_manager import *
from pylab import *
from global_variable import *
import pymysql
from py2neo import *
import json

# 连接Neo4j数据库
bgds_detail_inspection_graph=Graph("http://10.94.81.132:7474",auth=("neo4j","ABCabc123"))

node_baoguanhao = None
node_cangdanhao = None

# 建立节点
def buildNodes(nodeRecord):
    global node_baoguanhao, node_cangdanhao
    id = nodeRecord.identity
    data = {"id":id}
    datadict = dict(nodeRecord)
    name = list(nodeRecord.labels)[0]
    colors = {'报关单号': 'red', '舱单号': 'yellow', '查验任务编号': 'blue',
              '经营单位代码': 'antiquewhite', '申报单位代码': 'antiquewhite', '货主单位代码': 'antiquewhite',
              '经营单位法人证件号': 'aquamarine', '申报单位法人证件号': 'aquamarine', '贸易方式': 'blueviolet',
              '申报时间': 'coral', '进出境时间': 'coral', '中控时间': 'coral', '派单时间': 'coral',
              '车牌号': 'darkturquoise', '非内地车牌号': 'darkturquoise', '司机ID': 'darkturquoise', '进出口标记': 'grey',
              '当班科室': 'deeppink', '口岸当班科室': 'gainsboro',
              '布控科室': 'gold', '布控人代码': 'gold',
              '查验科室': 'lawngreen', '查验科长': 'lawngreen', '人工查验主查人员': 'lawngreen', '人工查验辅查人员': 'lawngreen',
              '机检科室': 'orangered', '机检科长': 'orangered', '机检人A': 'orangered', '机检人B': 'orangered'}
    if name is not None:
        value = datadict[name]
        data["name"] = name + " " + value
        data["key"] = name
        data["val"] = value
        if colors.__contains__(name):
            data["color"] = colors[name]
        else:
            data["color"] = "grey"
        if name == '报关单号':
            node_baoguanhao = id
        elif name == '舱单号':
            node_cangdanhao = id
    #print('datadict=',datadict)
    #data = {"id": nodeRecord.identity, "label": list(nodeRecord.labels)[0]}  # 将集合元素变为list，然后取出值
    #data = {"id": nodeRecord.identity, "name": list(nodeRecord.labels)[0]}  # 将集合元素变为list，然后取出值
    #data.update(datadict)
    #print('data:', data)
    return {"data": data}


#建边
def buildEdges(relationRecord):
    edge_dict = dict(relationRecord)
    #print("edge_dict=",edge_dict)
    type = list(relationRecord.types())
    data = {
        "source": relationRecord.start_node.identity,
        "target": relationRecord.end_node.identity,
        "name": type,
    }
    if 'weight' in edge_dict:
        data['weight'] = edge_dict['weight']
    return {"data": data}

# 返回点和边组成的json数据
def _main_graph(kv_dict={},limit=999,graph=bgds_detail_inspection_graph):
    print('_main_graph', kv_dict)

    mydb = pymysql.connect(**MYSQLCONFIG_DICT)
    sql_op_str="select 报关单号 from database_1.bgds_inspection_details_2020_view where 报关单号 is not null"
    for i in tuple(kv_dict):
        sql_op_str+=" and "+str(i)+"='"+str(kv_dict[i])+"'"

    if limit!=0:
        sql_op_str+=" limit "+str(limit)

    print(sql_op_str)

    bgds_df=pd.read_sql(sql_op_str,mydb)
    print('bgds_df=', bgds_df)

    #res_list=[]
    nodeList = []
    edgeList = []

    for index,row in bgds_df.iterrows():
        neo4j_op_str=""
        neo4j_op_str+="MATCH (n:`报关单号`{`报关单号`:'"+str(row['报关单号'])+"'})-[]-(m:`舱单号`)-[]-(p:`查验任务编号`)"
        neo4j_op_str+=""" OPTIONAL MATCH a=(n)--(neighbor1)
        OPTIONAL MATCH b=(m)--(neighbor2) where labels(neighbor2) <> ["报关单号"]
        OPTIONAL MATCH c=(p)--(neighbor3) where labels(neighbor3) <> ["报关单号"]
        with [a,b,c] as coll unwind coll as x with distinct x return NODES(x),RELATIONSHIPS(x)"""

        print(neo4j_op_str)
        rt_neo =graph.run(neo4j_op_str)

        for result in rt_neo:
            #print('result', result)
            for part in result:
                the_part = part[0]
                if isinstance(the_part, Node):
                    for elem in part:
                        nodeList.append(elem)
                else:
                    edgeList.append(the_part) # ???

    nodeList = list(set(nodeList))
    nodes = list(map(buildNodes, nodeList))

    tmp = list(map(buildEdges, edgeList))
    edges = []
    [edges.append(i) for i in tmp if i not in edges]
    return {"nodes": nodes, "edges": edges}

# 前端通过post请求此方法，继而调用main_graph函数得到节点和边的数据，并在前端中通过json_api和o2s将数据转为json格式
def post_graph(request=None):
    if request:
        # if request.content_type.startswith('application/json'):
        s = request.get_data()
        print('DEBUG data',s)
        data = json.loads(s)
        #return {"STS":"OK","data":data}
        return _main_graph(kv_dict=data)
    return {"STS":"KO","errmsg":"need POST params"}

#if __name__=='__main__':
#    res=_main_graph(kv_dict={'报关单号': "521320200630144656"})
#    print(res)
