#!/bin/env python3
###!/home/iprobe/program/anaconda3/bin/python3

from flask import *

import json

app = Flask(__name__)
#app.secret_key = "secret_key"

def build_rt(request, output):
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

import importlib, os
@app.route('/<c>.<m>', methods=['GET', 'POST','OPTIONS'])
def handle(c, m):
    try:
        cc = str(c)
        if cc!=os.path.basename(__file__).split('.')[0]:
            mm = str(m)
            if (mm == '__dict__'):
                output = "not allow {}".format(mm)
            else:
                ccc = importlib.import_module(cc)
                mmm = getattr(ccc, mm)
                output = mmm(request)
        else:
            output = "404 {}".format(cc)
    except Exception as ex:
        output = "err={}".format(str(ex))
    return build_rt(request, output)

@app.route('/')
def rt():
    rt = ''
    try:
        mdl = request.args.get('mdl', default=None)
        if mdl:
            importlib.reload(importlib.import_module(mdl))
        rt = request.args
    except Exception as ex:
        rt = {'errmsg':str(ex)}
    return build_rt(rt)
    
if __name__ == "__main__":
    #threading.Thread(target=main_thread).start()
    app.run(host='0.0.0.0', port=1234, debug=True)
    # app.run(host='0.0.0.0', port=1234)
#else:
    #FLASK_ENV=development FLASK_APP=flsk.py flask run --host 0.0.0.0 --port 1234

