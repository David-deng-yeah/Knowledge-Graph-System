import dba
dbsrc=dba.main('gbase.tmp') # raw src
db_name = 'dba'
dbtgt=dba.main('dba.tmp', db_name=db_name) # local db
import time

# import sys
# argv = sys.argv
# argc = len(argv)
# if(argc>1):
#     "IF NOT EXISTS"

##########################################################################################

#-- select `AGENT_CODE`,`AGENT_NAME`,`AGENT_SCC_CODE`,'ee' as SRC from app_db_cbee_zs.cbee_elist group by AGENT_CODE,AGENT_NAME,AGENT_SCC_CODE
sql = """
select `ASSURE_CODE` AS `CODE`,`ASSURE_NAME` AS `NAME`,'ASSURE_I' as SRC from app_db_cbec_zs.cbec_elist where ASSURE_NAME is not null group by ASSURE_CODE,ASSURE_NAME
"""
import pandas as pd
df = pd.read_sql(sql, con=dbsrc.engine)

def dosql(sql,dump=False,db=dbtgt):
    sql_lower = sql.strip().lower()
    print(sql)
    rt = db.engine.execute(sql)
    if sql_lower.startswith('select') or sql_lower.startswith('show') or sql_lower.startswith('explain'):
        rows = rt.fetchall()
        cols = rt.keys()
        if dump:
            print("rows,cols:",rows,cols)
        return rows,cols,rt
    else:
        if dump:
            print("rt:",rt)
        return None,None,rt
################################# dump to tmp table
tbl_name_work_tmp = 'tmp_{}_{}'.format('area',time.strftime("%m%d%H%M%S"))

df.to_sql(tbl_name_work_tmp, schema=db_name, index=False, if_exists='replace', con=dbtgt.engine)

# sync:
dosql("""
        INSERT INTO o_corp (`CODE`, `NAME`, `SRC`,`LMT`)
        SELECT `CODE`,`NAME`,`SRC`,NOW() AS LMT FROM {}
        ON DUPLICATE KEY UPDATE
        CODE=VALUES(CODE), NAME=VALUES(NAME), SRC=VALUES(SRC), LMT=NOW()
        """.format(tbl_name_work_tmp))

dosql('DROP TABLE {}'.format(tbl_name_work_tmp))

print("CORP(I+E):")
df = pd.read_sql("""
        select COUNT(*) C, GROUP_CONCAT(code) grp_code, GROUP_CONCAT(`SRC`) grp_src, `name` from o_corp group by `name` having c>1;
        """, con=dbtgt.engine);
print(df)
