import dba

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
        return (rows,cols,rt)
    else:
        if dump:
            print("rt:",rt)
        return (None,None,rt)

# NOTES: %% => % specially for sqlalchemy/pymysql...
[rows,cols,rt] = dosql("""
SELECT CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) AS tbl FROM information_schema.tables WHERE TABLE_NAME like '{tmp}' AND TABLE_SCHEMA = '{db_name}'
""".format(tmp='tmp_%%',db_name=db_name))
#print(rows)
[dosql('DROP TABLE {}'.format(row.tbl)) for row in rows]
