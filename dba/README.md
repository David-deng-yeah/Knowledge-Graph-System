# py class

* dba.py -- the db helper 
    * config: gbase.tmp and dba.tmp

# one off

```
corp\ -- pys for o_corp
    dba_agent.py
    dba_area.py
    dba_assure.py
    ...
csvgz\ -- pys for tbls/cols backup/restore
    dba_from_csvgz.py
    dba_to_csvgz.py
dba_clear_tmp.py -- clear tmp_% manually
```

# daily

```
stepX_*.py:
    remote data pre-processing (mostly the group/order)
```

# report

```
reports\
```


# lab

# tools

```
* mysqlproxy.sh -- to start a mysql-proxy to expose port 5258 of gbase (for quicker dev)
    *.lua
```

