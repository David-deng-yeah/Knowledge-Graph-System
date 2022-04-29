WORKNAME=$1

# WARNING: the $WORKNAME table should be created manualy first

cat ${WORKNAME}_export.sql | ../gbase_client.sh > $PWD/$WORKNAME.tmp

cat ${WORKNAME}_import.sql | ../dba_client.sh

cat ${WORKNAME}_post.sql | ../dba_client.sh dba

