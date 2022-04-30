#!/bin/env python3
###!/home/iprobe/program/anaconda3/bin/python3
from flask import Flask, abort, render_template, redirect, url_for, request, make_response,jsonify
import requests, json, os, time, random, threading
# import tableauserverclient as tsc

app = Flask(__name__)
app.secret_key = "secret_key"

# url of tableau server
# tableau服务器的ip地址
server_url = 'http://10.94.81.132'

import logic
import neo4j

# 用户信息类
class UserLoginInfo:
    username = ""
    password = ""
    lasttime = 0
    server = None
    def __init__ (self, username, password):
        self.username = username
        self.password = password
        self.server = tsc.Server(server_url)

login_lock = threading.Lock()
login_count = 0
login_infos = {}
login_name_id_map = {}

app_path = os.path.dirname(__file__)
# 图像路径
img_path = app_path + "/static/generated"
if not os.path.exists(img_path):
    os.makedirs(img_path)

def make_resp(request, output):
    resptext = None
    if 'callback' in request.args:
        resptext = request.args['callback'] + "(" + json.dumps(output) + ")"
    else:
        resptext = json.dumps(output)
    resp = make_response(resptext)
    resp.headers.add('Access-Control-Allow-Origin',"*")
    resp.headers.add('Access-Control-Allow-Methods',"GET,POST")
    resp.headers.add('Access-Control-Allow-Headers',"content-type,accept")
    return resp


import importlib
@app.route('/<c>.<m>', methods=['GET', 'POST','OPTIONS'])
def handle(c, m):
    try:
        global login_infos
        global login_name_id_map
        cc = str(c)
        if (cc=='logic' or cc=='neo4j'):
            mm = str(m)
            if (mm == '__dict__'):
                output = "not allow {}".format(mm)
            else:
                ccc = importlib.import_module(cc)
                mmm = getattr(ccc, mm)
                # tmp hack !!!!
                userid = None
                username = None
                server = None # tableau one
                if 'username' in request.args:
                    username = request.args["username"]
                    userid = login_name_id_map[username]
                if 'userid' in request.args:
                    userid = request.args["userid"]
                if userid and userid in login_infos:
                    userinfo = login_infos[userid]
                    server = userinfo.server
                request.username = username
                request.userid = userid
                request.server = server
                output = mmm(request)
        else:
            output = "unsupport {}".format(cc)
    except Exception as ex:
        output = "err={}".format(str(ex))
    return make_resp(request, output)

@app.route('/test', methods=['GET', 'POST','OPTIONS'])
def test():
    return make_resp(request, logic.test())

@app.route('/reload', methods=['GET', 'POST','OPTIONS'])
def reload():
    importlib.reload(importlib.import_module("logic"))
    importlib.reload(importlib.import_module("neo4j"))
    return make_resp(request, "ok")

# Route for handling the login page logic
# Checks if user exists and password matches
# 用以处理登录事件的路由，用以确定用户是否存在，并且密码是否配对
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global tableau_auth, login_lock, login_count, login_infos, login_lock, login_name_id_map
    username = None; password = None; userinfo = None
    token = None
    output = {}
    if 'username' in request.args:
        username = request.args['username']
        password = request.args['password']
        # 创建一个用户信息类
        userinfo = UserLoginInfo(username, password)
        tableau_auth = tsc.TableauAuth(username, password)
        try:
            rst_signin = userinfo.server.auth.sign_in(tableau_auth)
# wjc: wtf, this token is one-time-off??
##             # wjc: TODO is the token already inside the rst_signin ???!!!
##             print ("rst_signin=", rst_signin)
##             token_req = requests.post(server_url+"/trusted?username=" + username)
##             # 200 = OK in HTTP requests
##             if (token_req.status_code != 200 or token_req.text == '-1'):
##                 # output["error"] = "Failed to download a ticket from tableau server("+server_url+") for "+username+"."
##                 error = "Failed to download a ticket from tableau server("+server_url+") for "+username+"."
##                 # output["state"] = "failed"
##             else:
##                 # output["token"] = token_req.text
##                 # output["url"] = server_url
##                 # output["state"] = "succeeded"
##                 token = token_req.text
        except tsc.ServerResponseError:
            error = "Invalid Username or Password. Please try again."
    # elif "token" in request.form:
    #     tableau_auth = tsc.PersonalAccessTokenAuth(token_name=request.form['token_name'],
    #                                                personal_access_token=request.form['personal_access_token'],
    #                                                site_id=request.form['site_id'])
    #     try:
    #         server.auth.sign_in_with_personal_access_token(tableau_auth)
    #         accesstoken = request.form['personal_access_token']
    #     except tsc.ServerResponseError:
    #         error = "Invalid Token. Please try again."
    else:
        error = "Invalid login information."
    # 如果没出错误
    if error is None:
        login_lock.acquire()
        userid = "{}.{}".format(time.time(), login_count)
        userinfo.lasttime = time.time_ns()
        login_infos[userid] = userinfo
        login_name_id_map[username] = userid
        login_count += 1
        if (login_count>1000000):
            login_count = 0
        login_lock.release()
        output = {"state": "succeeded", "userid": userid, "username":username, "token": token}
    else:
        output = {"state": "failed", "error": error}
    # 生成返回数据报，包含登录状态，用户信息
    resp = make_resp(request, output)
    #time.sleep(2) # wjc tmp block a little ... wtf... too...
    return resp

# 用来处理用户登出的路由
@app.route('/logout')
def logout():
    global login_lock
    global login_infos
    output = {}
    if 'userid' in request.args:
        userid = request.args["userid"]
        login_lock.acquire()
        if userid in login_infos:
            userinfo = login_infos[userid]
            userinfo.server.auth.sign_out()
            del login_infos[userid]
            output = {"state": "succeeded"}
        else:
            output = {"state": "failed", "error": "login expired."}
        login_lock.release()
    else:
        output = {"state": "failed", "error": "userid is missing in the arguments."}
    return make_resp(request, output)

@app.route("/projects_data")
def projects_data():
    global login_infos
    if 'userid' in request.args:
        userid = request.args["userid"]
        if userid not in login_infos:
            return make_resp(request, {"state": "failed", "error": "not logged in"})
    else:
        return make_resp(request, {"state": "failed", "error": "missing userid"})

    userinfo = login_infos[userid]
    userinfo.lasttime = time.time_ns()

    all_projects_items, pagination_item = userinfo.server.projects.get()
    projects_by_id = dict()
    for x in all_projects_items:
        id = x.id
        if id not in projects_by_id:
            projects_by_id[id] = {"name": x.name, "description": x.description}

    return make_resp(request, {"state": "succeeded", "projects": projects_by_id})

@app.route("/workbooks_data")
def workbooks_data():
    global login_infos
    if 'userid' in request.args:
        userid = request.args["userid"]
        if userid not in login_infos:
            return make_resp(request, {"state": "failed", "error": "not logged in"})
    else:
        return make_resp(request, {"state": "failed", "error": "missing userid"})

    userinfo = login_infos[userid]
    userinfo.lasttime = time.time_ns()

    workbooks, pagination_item = userinfo.server.workbooks.get()

    workbook_data = []
    for x in workbooks:
        data = {}
        userinfo.server.workbooks.populate_preview_image(x)
        img_file_name = "{}.jpg".format(x.name)
        img_file_path = img_path + "/" + img_file_name
        # generate thumbnails of all workbooks
        with open(img_file_path, "wb") as img_file:
            img_file.write(x.preview_image)
        data["img_path"] = "/static/generated/" + img_file_name
        data["description"] = x.description or ""
        data["name"] = x.name or ""
        data["id"] = x.id
        data["created_at"] = x.created_at.strftime("%Y - %m - %d %H:%M:%S")
        data["project_id"] = x.project_id
        data["project_name"] = x.project_name
        workbook_data.append(data)

    return make_resp(request, {"state": "succeeded", "data": workbook_data})


@app.route("/views_data")
def views_data():
    global login_infos
    if 'userid' in request.args:
        userid = request.args["userid"]
        if userid not in login_infos:
            return make_resp(request, {"state": "failed", "error": "not logged in"})
    else:
        return make_resp(request, {"state": "failed", "error": "missing userid"})

    userinfo = login_infos[userid]
    userinfo.lasttime = time.time_ns()

    id = request.args.get("id")
    workbook = userinfo.server.workbooks.get_by_id(id)
    userinfo.server.workbooks.populate_views(workbook)
    all_data = []
    for x in workbook.views:
        data = {}
        # print("view x=", x)
        userinfo.server.views.populate_preview_image(x)
        img_file_name = "{}[{}].jpg".format(id, x.name)
        img_file_path = img_path + "/" + img_file_name
        # generate thumbnails of all views
        with open(img_file_path, "wb") as img_file:
            img_file.write(x.preview_image)
        data["img_path"] = "/static/generated/" + img_file_name
        data["name"] = x.name or ""
        data["id"] = x.id
        data["content_url"] = x.content_url
        data['workbook_id'] = x.workbook_id
        data['project_id'] = x.project_id
        all_data.append(data)
    return make_resp(request, {"state": "succeeded", "data": all_data})


# This is used to construct an url like this:
# https://tabserver/trusted/<ticket>/views/<content_url>
# the ticket can only be used once by one request
@app.route('/get_token')
def get_token():
    output = {}
    global login_infos, login_lock
    if 'userid' in request.args:
        userid = request.args["userid"]
        # Because token has access control problem, require logged in all the time.
        # 锁上后端线程，等待用户登录线程执行完毕
        login_lock.acquire()
        if userid in login_infos:
            userinfo = login_infos[userid]
            userinfo.lasttime = time.time_ns()
            username = userinfo.username
            # in order to make this post request, this web server should be added to trusted servers in TSM web.
            # use the username in cookie, which can support multiple browsers
            rst_token_req = requests.post(server_url+"/trusted?username=" + username)
            #print("debug rst_token_req", rst_token_req);
            # 200 = OK in HTTP requests
            if (rst_token_req.status_code != 200 or rst_token_req.text == '-1'):
                output["error"] = "Failed to download a ticket from tableau server("+server_url+") for "+username+"."
                output["state"] = "failed"
            else:
                output["token"] = rst_token_req.text
                output["url"] = server_url
                output["state"] = "succeeded"

            ###output["token"] = userinfo.server.auth_token
            ###output["url"] = server_url
            ###output["state"] = "succeeded"
        else:
            print("DEBUG login_infos", login_infos)
            output["state"] = "failed"
            output["error"] = "not logged in?"
        login_lock.release()
    else:
        output["state"] = "failed"
        output["error"] = "missing userid"
    return make_resp(request, output)

# 用以终止用户登录的线程
class LoginExpiryThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while(True):
            print("checking login expiry...")
            current_time = time.time_ns()
            login_lock.acquire()
            expired_ids = []
            for userid in login_infos:
                userinfo = login_infos[userid]
                if (current_time-userinfo.lasttime>1800*1000000000):
                    expired_ids.append(userid)
            for userid in expired_ids:
                userinfo = login_infos[userid]
                userinfo.server.auth.sign_out()
                del login_infos[userid]
                print("{}[{}] login expired.".format(userid, userinfo.username))
            login_lock.release()
            # wait for 5 minutes
            # the actual time of time.sleep may be shorter or longer.
            time.sleep(300)


if __name__ == "__main__":
    # run user login thread
    LoginExpiryThread().start()

    # run flask server
    app.run(host="0.0.0.0",port=5000, debug=True)
