import dba
#dbsrc=dba.main('gbase.tmp') # raw src
db_name = 'dba'
dbtgt=dba.main('dba.tmp', db_name=db_name) # local db

##########################################################################################
#dosql = dbtgt.engine.execute
def dosql(sql,dump=False):
    sql_lower = sql.strip().lower()
    print(sql_lower)
    rt = dbtgt.engine.execute(sql)
    if sql_lower.startswith('select') or sql_lower.startswith('show'):
        rows = rt.fetchall()
        cols = rt.keys()
        if dump:
            print("rows,cols:",rows,cols)
        return rows,cols,rt
    else:
        if dump:
            print("rt:",rt)
        return None,None,rt

#import time
#tbl_name_work_tmp = 'tmp_{}_{}'.format('sync',time.strftime("%m%d%H%M%S"))

import pandas as pd

sql = 'select * from gbasetbls'
#df = pd.read_csv('gbasetbls.csv')
df = pd.read_csv('gbasetbls.csv.gz',compression='gzip')
df.to_sql('gbasetbls_tmp', schema=db_name, index=False, if_exists='replace', con=dbtgt.engine)

sql = 'select * from gbasecols'
df = pd.read_csv('gbasecols.csv.gz',compression='gzip')
df.to_sql('gbasecols_tmp', schema=db_name, index=False, if_exists='replace', con=dbtgt.engine)

