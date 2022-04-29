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

###########################
import os
#os.system('gunzip -c gbasetbls.csv.gz > gbasetbls_old.csv.tmp')
#os.system('gunzip -c gbasecols.csv.gz > gbasecols_old.csv.tmp')

###########################
import pandas as pd

sql = 'select * from gbasetbls'
df = pd.read_sql(sql, con=dbtgt.engine)
df.to_table('gbasetbls.table',index=False)

sql = 'select * from gbasecols'
df = pd.read_sql(sql, con=dbtgt.engine)
df.to_table('gbasecols.table',index=False)


