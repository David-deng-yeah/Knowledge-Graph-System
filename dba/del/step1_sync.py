import dba
dbsrc=dba.main('gbase.tmp') # raw src
sql = """
SELECT
TABLE_SCHEMA as db,
TABLE_NAME as tbl,
UPDATE_TIME AS lmt
FROM information_schema.tables
WHERE TABLE_SCHEMA not in ('information_schema','performance_schema','mysql','sys')
ORDER BY lmt desc
"""
import pandas as pd
# rst=dbsrc.engine.execute(sql)
# df = pd.DataFrame(data=rst.fetchall())
# df.columns = rst.keys()
df = pd.read_sql(sql, con=dbsrc.engine)

#print(df)
db_name = 'dba'
dbtgt=dba.main('dba.tmp', db_name=db_name) # local db

import time
tbl_name_work_tmp = 'tmp_{}_{}'.format('sync',time.strftime("%m%d%H%M%S"))
#df.to_csv('tbl.csv')
df.to_sql(tbl_name_work_tmp, schema=db_name, index=False, if_exists='replace', con=dbtgt.engine)

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

# add index for join
dosql('alter table {} add index tmp_db_tbl (db(64),tbl(128))'.format(tbl_name_work_tmp))

# sync remote (lmt) => local(rmt_lmt) for later comparing/cal_cols
dosql("""
        select * from
        gbasetbls myt right outer join {} rmt on myt.db=rmt.db and myt.tbl=rmt.tbl
        where myt.db is null or myt.tbl is null or myt.lmt is null or (myt.rmt_lmt<>rmt.lmt)
        """.format(tbl_name_work_tmp))
dosql("""
        INSERT INTO gbasetbls (db,tbl,rmt_lmt)
        SELECT rmt.db,rmt.tbl,rmt.lmt as rmt_lmt FROM
        gbasetbls myt right outer join {} rmt on myt.db=rmt.db and myt.tbl=rmt.tbl
        where myt.db is null or myt.tbl is null or myt.lmt is null or (myt.rmt_lmt<>rmt.lmt)
        ON DUPLICATE KEY UPDATE
        db=VALUES(db), tbl=VALUES(tbl), rmt_lmt=VALUES(rmt_lmt)
        """.format(tbl_name_work_tmp))

dosql('DROP TABLE {}'.format(tbl_name_work_tmp))

# warning full cols around 31k, so don't call too much for sync....
sql_cols = """
SELECT
TABLE_SCHEMA as db,
TABLE_NAME as tbl,
COLUMN_NAME as col,
DATA_TYPE as type,
CHARACTER_MAXIMUM_LENGTH as len
FROM information_schema.columns
WHERE TABLE_SCHEMA not in ('information_schema','performance_schema','mysql','sys')
"""
dfcols = pd.read_sql(sql_cols, con=dbsrc.engine)
tbl_name_work_tmp = 'tmp_{}_{}'.format('cols',time.strftime("%m%d%H%M%S"))
dfcols.to_sql(tbl_name_work_tmp, schema=db_name, index=False, if_exists='replace', con=dbtgt.engine)
dosql('alter table {} add index tmp_db_tbl_col (db(64),tbl(128),col(128))'.format(tbl_name_work_tmp))
dosql("""
        INSERT INTO gbasecols (db,tbl,col,type,len)
        SELECT rmt.db,rmt.tbl,rmt.col,rmt.type,rmt.len FROM
        gbasecols myt right outer join {} rmt on myt.db=rmt.db and myt.tbl=rmt.tbl and myt.col=rmt.col
        where myt.db is null or myt.tbl is null or myt.col is null
        ON DUPLICATE KEY UPDATE
        db=VALUES(db), tbl=VALUES(tbl), col=VALUES(col), type=VALUES(type), len=VALUES(len)
        """.format(tbl_name_work_tmp))
dosql('DROP TABLE {}'.format(tbl_name_work_tmp))

###############################################################################################
#dosql('select count(*) from gbasetbls where lmt is null or lmt<>rmt_lmt',dump=True)

[rows,cols,rst] = dosql('select db,tbl,rmt_lmt from gbasetbls where lmt is null or lmt<>rmt_lmt'
        +' LIMIT 9999')

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


