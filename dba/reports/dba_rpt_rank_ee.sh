## step 1: sync from remote
#echo "SELECT DATE_FORMAT(create_date,'%Y%m01') yyyymm01, COUNT(1) c, SUM(qty) s, sum(TOTAL_PRICE) ts, h_s_code,country FROM app_db_cbee_zs.cbee_elist_item GROUP BY h_s_code,yyyymm01,country" | ./gbase_sql.sh | mysql --host=127.0.0.1 --port=3306 --user=root --password=szu -e "load data local infile '/dev/stdin' replace into table dba.rpt_ee_yyyymm_code_country ignore 1 lines (yyyymm01,c,s,ts,h_s_code,country) ;"

echo "SELECT DATE_FORMAT(create_date,'%Y%m01') yyyymm01, COUNT(1) c, SUM(qty) s, sum(TOTAL_PRICE) ts, h_s_code,country FROM app_db_cbee_zs.cbee_elist_item GROUP BY h_s_code,yyyymm01,country" | ./gbase_sql.sh > $PWD/export_ee_yyyymm01_cty.tmp

mysql --host=127.0.0.1 --port=3306 --user=root --password=szu -e "load data local infile '$PWD/export_ee_yyyymm01_cty.tmp' replace into table dba.rpt_ee_yyyymm_code_country ignore 1 lines (yyyymm01,c,s,ts,h_s_code,country) ;"

# step 2: calc local
# cat dba_rpt_rank_ee.sql | mysql --host=127.0.0.1 --port=3306 --user=root --password=szu
cat dba_rpt_rank_ee.sql | ./mysql3306.sh dba

