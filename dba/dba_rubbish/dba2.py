'''
    DataBase Assistant
    Author: Wanjo
    Version: 20201008
'''
#########################################################################
from builtins import hash,print
import time

# private data
_ = {
    'time_init':time.time()  # for performance profiling
}

# first day of the month which nth before now, it points to current when n=0
def get_yyyymm01(n=0):
    yyyy, mm, dd, hh, nn = time.strftime("%Y,%m,%d,%H,%M").split(',')
    _yyyy=int(yyyy); _mm=int(mm); _dd=int(dd)
    return '{}{:02d}{:02d}'.format(_yyyy+(_mm-1-n)//12,(_mm-1-n)%12,1)

class main:
#########################################################################
    def __init__(self, dbstr_file=None,dbstr="{db_protocol}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset={db_charset}",
            db_protocol='mysql', db_host='10.54.202.211', db_port=5258, db_user='app_gbase_zhjj', db_pass='', db_name='', db_charset='utf8', dump=False):
        #time_init = time.time()
        _hash = hash(self)
        _[_hash]={}

        #################################################################
        try:
            from sqlalchemy import create_engine #, MetaData, Table, select
            import pymysql
            pymysql.install_as_MySQLdb()
            if dbstr_file:
                with open(dbstr_file, 'r') as _file:
                    dbstr = _file.read().replace('\n', '')
            #from urllib import quote_plus as urlquote # py2
            from urllib.parse import quote_plus as urlquote # py3
            _dbstr = dbstr.format(db_protocol=db_protocol,db_user=db_user,db_pass=urlquote(db_pass),db_host=db_host,db_port=db_port,db_name=db_name,db_charset=db_charset)
            if dump:
                print('_dbstr', _dbstr)
            self.engine = engine = create_engine(_dbstr)
        except Exception as ex:
            print(ex)

        self.get_yyyymm01 = get_yyyymm01

    def __del__(self): _.pop(hash(self), None)

    def dosql(self, sql, args=None, dump=False):
        sql_lower = sql.strip().lower()
        if dump:
            print(sql)
        rt = self.engine.execute(sql)
        rows = None
        cols = None
        if sql_lower.startswith('select') or sql_lower.startswith('show') or sql_lower.startswith('explain'):
            rows = rt.fetchall()
            cols = rt.keys()
        return rows,cols,rt
#########################################################################
if __name__ == "__main__":
    #print(main().get_yyyymm01())
    #from dba import main as dba;db=dba(dbstr_file='db.tmp')
    db=main(dbstr_file='dba2.tmp')
    print(db.get_yyyymm01())
    import sys
    argv = sys.argv
    argc = len(sys.argv)

    if argc>1:
        sql = argv[1]
    else:
        sql = """
        SELECT CONCAT(TABLE_SCHEMA,',',TABLE_NAME) AS tbl,
        UPDATE_TIME AS lmt
        FROM information_schema.tables
        WHERE TABLE_SCHEMA not in ('information_schema','performance_schema','mysql','sys')
        ORDER BY lmt desc
        """
    print(sql,'=>')
    # print(len(db.engine.execute(sql).fetchall()))
    print(db.dosql(sql))
