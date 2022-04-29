import dba

db=dba.main('gbase.tmp') # local db

[rows,cols,rt] = db.dosql("show processlist")
print(rows)
for row in rows:
    id = row['Id']
    user = row['User']
    Time = int(row['Time'])
    Command = row['Command']
    if Command=='Sleep' and Time>999:
        db.dosql('KILL {id}'.format(id=id))
    else:
        print("skip", row)
#[dosql('DROP TABLE {}'.format(row.tbl)) for row in rows]
