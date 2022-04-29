#echo sudo me if need run as --user=$USER

CONFDIR=$PWD

cd $HOME/mysql-proxy-0.8.5-linux-glibc2.3-x86-64bit/

#./bin/mysql-proxy --defaults-file=$CONFDIR/conf_mysqlproxy_dev --user=$USER
./bin/mysql-proxy --proxy-lua-script=$CONFDIR/mysqlproxy.lua --proxy-address=0.0.0.0:5257 --proxy-backend-addresses=10.54.202.211:5258 --plugins=proxy --keepalive=true $*

cd $CONFDIR
