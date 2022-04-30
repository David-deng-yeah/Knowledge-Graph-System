import time, os
init_time = time.time()

import tableauserverclient as tsc
# url of tableau server
server_url = 'http://10.94.81.132'

def test(request):
    print("ok logic.test()")
    return ("OK"+str(init_time))

#import dba
from dba.dba import main as dba
from dba.dba_rubbish.dba2 import main as dba2

import json
#db = dba.main(dbstr_file='/home/gitlocal/web/dba.tmp')

# 用于执行sql
db1 = dba(dbstr_file='/home/gitlocal/web/dba.tmp')
db2 = dba2(dbstr_file='/home/gitlocal/web/dba2.tmp')
#sql = "show databases;"

g_user_view_map = {}

def build_view_map(server):
    rt = {}
    erra = []
    # 处理分页项目
    # TODO need to handl pagination_item in future
    workbooks, pagination_item = server.workbooks.get()
    for x in workbooks:
        try:
            server.workbooks.populate_views(x)
            for view_item in x.views:
                view_id = view_item.id
                #TODO check content_url None later
                view_content_url = view_item.content_url.replace("/sheets/", "/")
                rt[view_content_url] = view_id
        except Exception as ex:
            #print (ex)
            erra.append(str(ex))
    rt['erra'] = erra
    return rt

def check_view(request):
    global g_user_view_map
    rt = {}
    username = request.username
    userid = request.userid
    server = request.server

    view_content_url = None
    if 'content_url' in request.args:
        view_content_url = request.args['content_url']

    view_id = None
    if 'view_id' in request.args:
        view_id = request.args['view_id']

    user_map = None
    if userid in g_user_view_map:
        #user_map = g_user_view_map[userid]
        print(userid)
    else:
        # get user map
        user_map = build_view_map(server)
        g_user_view_map[userid] = user_map

    user_map = g_user_view_map[userid]
    view_item = None
    if user_map:
        if view_content_url in user_map:
            view_item = user_map[view_content_url]
            #if view_item:
                # todo get token
        rt['view'] = view_item

    return rt

# 列出服务器的视图
def list_view(request):
    username = request.username
    userid = request.userid
    flg_server = None
    server = request.server
    return build_view_map(server)
    # rows = []
    # if server:
    #     flg_server = True
    #     workbooks, pagination_item = server.workbooks.get()
    #     workbook_data = []
    #     for x in workbooks:
    #         # data = {}
    #         # # data["img_path"] = "/static/generated/" + img_file_name
    #         # data["description"] = x.description or ""
    #         # data["name"] = x.name or ""
    #         # data["id"] = x.id
    #         # # data["created_at"] = x.created_at.strftime("%Y - %m - %d %H:%M:%S")
    #         # data["project_id"] = x.project_id
    #         # data["project_name"] = x.project_name
    #         # # rows.append(x)
    #         # rows.append(data)
    #         try:
    #             server.workbooks.populate_views(x)
    #             for view_item in x.views:
    #                 view_id = view_item.id
    #                 view_content_url = view_item.content_url
    #                 rows.append({
    #                         'id':view_id,
    #                         'content_url':view_content_url,
    #                         })
    #             #    data = {
    #             #        'id':view_item['id'],
    #             #        'content_url':view_item['content_url'],
    #             #    }
    #             #    rows.append(data)
    #         except Exception as ex:
    #             rows.append({'errmsg':str(ex)})

    # # workbook = userinfo.server.workbooks.get_by_id(workbook_id)
    # # userinfo.server.workbooks.populate_views(workbook)
    # # all_data = []
    # # for view_item in workbook.views:
    # #

    # return {'STS':'TOOD', 'username': username, 'userid': userid, "flg_server": flg_server, 'rows':rows}

#children = []
def get_routers(request):
    sql = """
    select * from web.tmp order by srt,id asc;
    """ #.format()
    #print(db.dosql(sql))
    # 进行数据库查询
    rows,cols,rt = db1.dosql(sql)
    #print(rows)
    #print(cols)
    #print(rt)
    #json_data = []
    #for row in rows:
    #    json_data.append(dict(zip(cols, row)))
    #print(json_data)
    #print(json.dumps(json_data))

    routers = {}
    for row in rows:
        #print(row)
        # [_id, _pid, _path, _title, _url] = row
        _id = row[0]
        _srt = row[1]
        _self_key = row[2]
        _parent_key = row[3]
        _path = row[4]
        _component = row[5]
        _title = row[6]
        _url = row[7]
        _db = row[8]
        _sql = row[9]

        if _parent_key:
            _child = {"path":_path, "component":_component, "meta":{"id":_id, "srt":_srt, "self_key":_self_key, "parent_key":_parent_key, "title":_title, "url":_url, "db":_db, "sql_sentence":_sql}}
            the_line = routers[_parent_key]
            if the_line.__contains__('children'):
                _child_a = the_line['children'] # if js: _child_a = the_line['child'] || [];
            else:
                _child_a = []
            _child_a.append(_child)
            the_line['children'] = _child_a
            #routers[_pid] = the_line
            #routers.append(the_line)
        else:
            routers[_self_key] = {
                 "path":_path, "component":_component, "meta":{"id":_id, "srt":_srt, "self_key":_self_key, "parent_key":_parent_key, "title":_title, "url":_url, "db":_db, "sql_sentence":_sql}
            }
            #routers.append({
            #    "path":_path, "component":_component, "meta":{"title":_title, "url":_url}
            #})

    _routers = []
    for key in routers:
        _routers.append(routers[key])
    #print(routers)
    results = {"router": _routers}
    return results

# 返回router
def routers_show(request):
    sql = """
    select * from web.tmp order by srt,id asc;
    """ #.format()
    # 进行数据库查询
    rows,cols,rt = db1.dosql(sql)
    routers = []
    for row in rows:
        _id = row[0]
        _srt = row[1]
        _self_key = row[2]
        _parent_key = row[3]
        _path = row[4]
        _component = row[5]
        _title = row[6]
        _url = row[7]
        _db = row[8]
        _sql = row[9]

        routers.append({
            "id":_id, "srt":_srt, "self_key":_self_key, "parent_key":_parent_key, "path":_path, "component":_component, "title":_title, "url":_url, "db":_db, "sql_sentence":_sql, "disable": True
        })
    return routers

# 根据request，通过sql向向web.tmp中插入数据
def routers_insert(request):
    s = request.get_data()
    if not s:
      return {"sts":'ko', 'errmsg':'need post data'}

    print('DEBUG data',s)
    data = json.loads(s)
    #parent_id, path, component, title, url = data

    #if not data['parent_id']:
    #    parent_id = 0
    #else:
    #    parent_id = data['parent_id']
    #parent_id = data['parent_id']
    self_key = data['self_key']
    srt = data['srt']
    parent_key = data['parent_key']
    path = data['path']
    component = data['component']
    title = data['title']
    url = data['url']
    db = data['db']
    sql_sentence = data['sql_sentence']

    #sql = """
    #insert into web.tmp (title) values('tmp111')
    #""" #.format()
    #print(db.dosql(sql))

    #py2
    #sql = "insert into web.tmp values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')"%(parent_id, path, component, title, url)

    # py3 syntax:
    #sql = "insert into web.tmp (parent_id, path, component, title, url) values ('{parent_id}', '{path}', '{component}', '{title}', '{url}')".format(parent_id=parent_id, path=path, component=component, title=title, url=url)
    sql = "insert into web.tmp (self_key, parent_key, path, component, title, url, db, sql_sentence) values ('{self_key}', '{srt}', '{parent_key}', '{path}', '{component}', '{title}', '{url}', '{db}', '{sql_sentence}')".format(self_key=self_key, srt=srt, parent_key=parent_key, path=path, component=component, title=title, url=url, db=db, sql_sentence=sql_sentence)
    rows,cols,rt = db1.dosql(sql)
    #
    af = rt.rowcount
    sts = 'ko'
    if af>0:
      sts = 'ok'
    # update ... where ... => af = 1
    #
    rst = {"sts": sts, "af": af}
    return rst

def routers_delete(request):
    s = request.get_data()
    if not s:
      return {"sts":'ko', 'errmsg':'need post data'}

    print('DEBUG data',s)
    data = json.loads(s)

    id = data['id']
    srt = data['srt']
    self_key = data['self_key']
    parent_key = data['parent_key']
    path = data['path']
    component = data['component']
    title = data['title']
    url = data['url']
    db = data['db']
    sql_sentence = data['db']

    #sql = """
    #insert into web.tmp (title) values('tmp111')
    #""" #.format()
    #print(db.dosql(sql))

    #py2
    #sql = "insert into web.tmp values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')"%(parent_id, path, component, title, url)

    # py3 syntax:
    #sql = "insert into web.tmp (parent_id, path, component, title, url) values ('{parent_id}', '{path}', '{component}', '{title}', '{url}')".format(parent_id=parent_id, path=path, component=component, title=title, url=url)
    #sql = "insert into web.tmp (self_key, parent_key, path, component, title, url) values ('{self_key}', '{parent_key}', '{path}', '{component}', '{title}', '{url}')".format(self_key=self_key, parent_key=parent_key, path=path, component=component, title=title, url=url)
    sql = "delete from web.tmp where id={id}".format(id=id)
    rows,cols,rt = db1.dosql(sql)
    #
    af = rt.rowcount
    sts = 'ko'
    if af>0:
      sts = 'ok'
    # update ... where ... => af = 1
    #
    rst = {"sts": sts, "af": af}
    return rst

def routers_update(request):
    s = request.get_data()
    if not s:
      return {"sts":'ko', 'errmsg':'need post data'}

    print('DEBUG data',s)
    data = json.loads(s)

    id = data['id']
    srt = data['srt']
    self_key = data['self_key']
    parent_key = data['parent_key']
    path = data['path']
    component = data['component']
    title = data['title']
    url = data['url']
    db = data['db']
    sql_sentence = data['sql_sentence']

    #sql = """
    #insert into web.tmp (title) values('tmp111')
    #""" #.format()
    #print(db.dosql(sql))

    #py2
    #sql = "insert into web.tmp values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')"%(parent_id, path, component, title, url)

    # py3 syntax:
    #sql = "insert into web.tmp (parent_id, path, component, title, url) values ('{parent_id}', '{path}', '{component}', '{title}', '{url}')".format(parent_id=parent_id, path=path, component=component, title=title, url=url)
    #sql = "insert into web.tmp (self_key, parent_key, path, component, title, url) values ('{self_key}', '{parent_key}', '{path}', '{component}', '{title}', '{url}')".format(self_key=self_key, parent_key=parent_key, path=path, component=component, title=title, url=url)
    sql = "update web.tmp set self_key='{self_key}', srt='{srt}', parent_key='{parent_key}', path='{path}', component='{component}', title='{title}', url='{url}', db='{db}', sql_sentence='{sql_sentence}' where id={id}".format(self_key=self_key, srt=srt, parent_key=parent_key, path=path, component=component, title=title, url=url, db=db, sql_sentence=sql_sentence, id=id)
    rows,cols,rt = db1.dosql(sql)
    #
    af = rt.rowcount
    sts = 'ko'
    if af>0:
      sts = 'ok'
    # update ... where ... => af = 1
    #
    rst = {"sts": sts, "af": af}
    return rst

# 从数据库中查询数据
def sql_select_column(request):
    s = request.get_data()
    if not s:
      return {"sts":'ko', 'errmsg':'need post data'}

    print('DEBUG data',s)
    data = json.loads(s)
    _dba = data['_dba']
    sql_sentence = data['sql_sentence']

    sql = """
    {sql_sentence}
    """ .format(sql_sentence=sql_sentence)

    #sql = """
    #select 进出境时间,进出口标记,出入境口岸,是否查验,经营单位名称 from database_1.bgds_inspection_details_2019_2020ne limit 10;
    #"""

    # mysql的话就从db1中及进行查询
    if _dba == 'mysql':
        rows,cols,rt = db1.dosql(sql)
    else:
        rows,cols,rt = db2.dosql(sql)
    sql_data = []
    for row in rows:
        row_dict = {}
        col_array = []
        for i,col in enumerate(cols):
            row_dict[col] = str(row[i])
            col_array.append(col)
        sql_data.append(row_dict)
    return {'sql_data': sql_data, 'col_array': col_array}

def ver(self):
    return {'STS':'OK', 'tm':time.time(), 'name':__name__, 'file':os.path.basename(__file__)}
