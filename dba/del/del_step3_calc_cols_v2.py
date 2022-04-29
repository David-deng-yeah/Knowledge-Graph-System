'''
    this script NOT good for big table of gbase, because it spend toooo much time on sending-task-to-gnodes when the select-union sql become big.....
'''
# TODO argv[1] => M-sampling
import dba

dbsrc=dba.main('gbase.tmp') # raw src
db_name = 'dba'
dbtgt=dba.main('dba.tmp', db_name=db_name) # local db

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
[rows,cols,rst] = dbsrc.dosql("""
        SELECT TABLE_SCHEMA as db, TABLE_NAME as tbl, COLUMN_NAME as col, DATA_TYPE as type, CHARACTER_MAXIMUM_LENGTH as len
        FROM information_schema.columns
        WHERE TABLE_SCHEMA='{db}' AND TABLE_NAME like '{tbl}'
        AND DATA_TYPE not in ('datatime','date','text','blob','longblob')
        AND COLUMN_NAME not in ('id','lmt')
        """.format(db=db,tbl=tbl) #,dump=True
        )

#g_limit = 199
g_limit = 99

_ = {"num":1} # counter
skip_a = ['datetime','date','text','blob','longblob']

sql_a = []

def handle(rmt_row):
    #print("g_limit=",g_limit);
    _db_name = rmt_row.db
    _tbl_name = rmt_row.tbl
    _col_name = rmt_row.col
    _len = rmt_row.len
    _type = rmt_row.type

    sql = """SELECT COUNT(1) grp,'{col}' AS `col` FROM (SELECT COUNT(1) FROM `{db}`.`{tbl}` GROUP BY `{col}` LIMIT 999) t
    """.format(db=_db_name,tbl=_tbl_name,col=_col_name)
    sql_a.append(sql)
#    # TODO _fam = rmt_row.fam (full/auto/manually sampling)
#    if not _len:
#        _len = 0
#
#    if True:
#    #if _len>99:
#    #    # sampling for _fam
#    #    print("tmp skip(len)", _db_name, _tbl_name, _col_name, _type, _len)
#    #else: # {
#        print(_['num'])
#        if skip_a.__contains__(_type):
#            # TODO sampling for _fam
#            print("tmp skip", _db_name, _tbl_name, _col_name, _type, _len)
#        else:
#            # TODO improve: multi-group by building sql in once, and then calc the len(rows)=>grp, and also build sampling data...?
#            #'select count(*) grp from (select count(`{col}`) c from {db_tbl} group by `{col}` order by c desc LIMIT {limit}) ggg'
#            #'select count(*) grp from (select `{col}` col from (select * from {db_tbl} limit 999) group by `{col}` LIMIT {limit}) ggg'
#            [rows,cols,rst] = dosql("""
#                    select count(*) grp from (select `{col}` from (select `{col}` from {db_tbl} limit 999) ttt group by `{col}`) ggg 
#                    """.format(col=_col_name,db_tbl=_db_name+'.'+_tbl_name,limit=g_limit), db=dbsrc)
#
#            grp = rows[0]['grp']
#            if grp>=99:
#                print("skip grp:", grp)
#                grp = 99
#            else:
#                print("init grp:", grp)
#                [rows,cols,rst] = dosql("""
#                        select count(*) grp from (select `{col}` from {db_tbl} group by `{col}` limit 999) ggg
#                        """.format(col=_col_name,db_tbl=_db_name+'.'+_tbl_name,limit=g_limit), db=dbsrc)
#                grp = rows[0]['grp']
#
#            # TODO if grp<99: full ...
#            # else: auto sample, (manually for speicified)
#            dosql("""
#                    INSERT INTO gbasecols (db,tbl,col,type,len,grp,lmt)
#                    SELECT '{db}' as db, '{tbl}' as tbl, '{col}' as col, '{type}' as type, '{len}' as len, '{grp}' as grp, NOW() as lmt
#                    ON DUPLICATE KEY UPDATE
#                    db=VALUES(db), tbl=VALUES(tbl), col=VALUES(col), type=VALUES(type), len=VALUES(len), grp=VALUES(grp), lmt=VALUES(lmt)
#                    """.format(db=rmt_row.db,tbl=rmt_row.tbl,col=rmt_row.col,type=_type,len=_len,grp=grp))
    # }
    _['num']+=1
    
[ handle(row) for row in rows ]

# TODO add .tbl_lmt, group (using group by, but need to sampling for bigtables)
# e.g. riskh2000_extr.occ_receipt


sql=" UNION ".join(sql_a)

print(sql)
print('len(sql)=',len(sql))

import time
print(time.time())
print(dbsrc.dosql(sql))
print(time.time())


