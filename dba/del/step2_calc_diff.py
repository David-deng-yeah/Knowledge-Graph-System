import dba

dbsrc=dba.main('gbase.tmp') # raw src
db_name = 'dba'
dbtgt=dba.main('dba.tmp', db_name=db_name) # local db
import time

##  tbl_name_work_tmp = 'tmp_{}_{}'.format('sync',time.strftime("%m%d%H%M%S"))
##########################################################################################
def dosql(sql,dump=False, db=dbtgt):
    sql_lower = sql.strip().lower()
    print(sql_lower)
    rt = db.engine.execute(sql)
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
##########################################################################################

[rows,cols,rst] = dosql('select db,tbl,rmt_lmt from gbasetbls where lmt is null or lmt<>rmt_lmt'
        +' LIMIT 2999')

def handle(rmt_row):
    _db_name = rmt_row.db
    _tbl_name = rmt_row.tbl
    _tbl_lmt = rmt_row.rmt_lmt
    print(_db_name,_tbl_name,_tbl_lmt)
    [rows,cols,rst] = dosql('select count(*) c from {dbname}.{tblname}'.format(_tbl_name,dbname=_db_name,tblname=_tbl_name),
            db=dbsrc, dump=True)
    [ dosql("""
        update gbasetbls set c={c}, lmt='{rmt_lmt}' where db='{db}' and tbl='{tbl}'
            """.format(c=row.c,rmt_lmt=_tbl_lmt,db=_db_name,tbl=_tbl_name)) for row in rows ]
    
[ handle(row) for row in rows ]

