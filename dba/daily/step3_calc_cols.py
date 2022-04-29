# TODO argv[1] => M-sampling
import sys
sys.path.append("..")
from dba import main as dba

dbsrc=dba('../gbase.tmp') # raw src
db_name = 'dba'
dbtgt=dba('../dba.tmp', db_name=db_name) # local db

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
  
# TODO play with cols of tbl (argv[1])
import sys
argv = sys.argv
argc = len(argv)
if argc>1:
    db  = argv[1]
    if argc>2:
        tbl = argv[2]
    else:
        tbl = '%%'
else:
    print("Usage: py $me $db [$tbl]")
    exit()
print("db=",db,"tbl=",tbl)

#### WHERE TABLE_SCHEMA not in ('information_schema','performance_schema','mysql','sys')
[rows,cols,rst] = dosql("""
        SELECT TABLE_SCHEMA as db, TABLE_NAME as tbl, COLUMN_NAME as col, DATA_TYPE as type, CHARACTER_MAXIMUM_LENGTH as len
        FROM information_schema.columns
        WHERE TABLE_SCHEMA='{db}' AND TABLE_NAME like '{tbl}'
        """.format(db=db,tbl=tbl),db=dbsrc #,dump=True
        )
'''
e.g.
rows,cols: [(None, 'riskh2000_extr', 'ram_rg_cop_owner', 'RAM_ID', 1, None, 'YES', 'varchar', 18, 54, None, None, 'utf8', 'utf8_general_ci', 'varchar(18)', '', '', 'select', '')] ['TABLE_CATALOG', 'TABLE_SCHEMA', 'TABLE_NAME', 'COLUMN_NAME', 'ORDINAL_POSITION', 'COLUMN_DEFAULT', 'IS_NULLABLE', 'DATA_TYPE', 'CHARACTER_MAXIMUM_LENGTH', 'CHARACTER_OCTET_LENGTH', 'NUMERIC_PRECISION', 'NUMERIC_SCALE', 'CHARACTER_SET_NAME', 'COLLATION_NAME', 'COLUMN_TYPE', 'COLUMN_KEY', 'EXTRA', 'PRIVILEGES', 'COLUMN_COMMENT']
'''

_ = {"num":1} # counter
g_limit = 999

skip_a = ['datetime','date','text','blob','longblob']

def handle(rmt_row):
    _db_name = rmt_row.db
    _tbl_name = rmt_row.tbl
    _col_name = rmt_row.col
    _len = rmt_row.len
    _type = rmt_row.type

#### delete later
####    if skip_a.__contains__(_type):
####        # TODO sampling for _fam
####        print("tmp skip", _db_name, _tbl_name, _col_name, _type, _len)
####    #else:
####        #print(_type)
####
####    return
    # TODO _fam = rmt_row.fam (full/auto/manually sampling)
    if not _len:
        _len = 0

    if True:
    #if _len>99:
    #    # sampling for _fam
    #    print("tmp skip(len)", _db_name, _tbl_name, _col_name, _type, _len)
    #else: # {
        print(_['num'])
        if skip_a.__contains__(_type):
            # TODO sampling for _fam
            print("tmp skip", _db_name, _tbl_name, _col_name, _type, _len)
        else:
            [rows,cols,rst] = dosql("""
                    select count(*) grp from (select `{col}` from (select `{col}` from {db_tbl} limit 999) ttt group by `{col}`) ggg 
                    """.format(col=_col_name,db_tbl=_db_name+'.'+_tbl_name), db=dbsrc)

            grp = rows[0]['grp']
            if grp>=g_limit:
                print("skip grp:", grp)
            else:
                print("init grp:", grp)
                [rows,cols,rst] = dosql("""
                        select count(*) grp from (select `{col}` from {db_tbl} group by `{col}` limit 999) ggg
                        """.format(col=_col_name,db_tbl=_db_name+'.'+_tbl_name), db=dbsrc)
                grp = rows[0]['grp']

            # TODO (step5) sampling full or selected
            dosql("""
                    INSERT INTO gbasecols (db,tbl,col,type,len,grp,lmt)
                    SELECT '{db}' as db, '{tbl}' as tbl, '{col}' as col, '{type}' as type, '{len}' as len, '{grp}' as grp, NOW() as lmt
                    ON DUPLICATE KEY UPDATE
                    db=VALUES(db), tbl=VALUES(tbl), col=VALUES(col), type=VALUES(type), len=VALUES(len), grp=VALUES(grp), lmt=VALUES(lmt)
                    """.format(db=rmt_row.db,tbl=rmt_row.tbl,col=rmt_row.col,type=_type,len=_len,grp=grp))
    # }
    _['num']+=1
    
[ handle(row) for row in rows ]

# TODO add .tbl_lmt, group (using group by, but need to sampling for bigtables)
# e.g. riskh2000_extr.occ_receipt


















