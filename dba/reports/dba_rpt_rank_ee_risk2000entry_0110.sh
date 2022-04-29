## step 1: sync from remote
#echo "SELECT DATE_FORMAT(create_date,'%Y%m01') yyyymm01, COUNT(1) c, SUM(qty) s, sum(TOTAL_PRICE) ts, h_s_code,country FROM app_db_cbee_zs.cbee_elist_item GROUP BY h_s_code,yyyymm01,country" | ./gbase_sql.sh | mysql --host=127.0.0.1 --port=3306 --user=root --password=szu -e "load data local infile '/dev/stdin' replace into table dba.rpt_ee_yyyymm_code_country ignore 1 lines (yyyymm01,c,s,ts,h_s_code,country) ;"

# echo "SELECT DATE_FORMAT(gbetl_datetime,'%Y%m01') yyyymm01, COUNT(1) c, SUM(G_QTY) s, sum(DECL_TOTAL) ts, CODE_TS as h_s_code,ORIGIN_COUNTRY as country FROM riskh2000_extr.entry_list GROUP BY h_s_code,yyyymm01,country" | ./gbase_sql.sh > $PWD/export_ee_yyyymm01_cty_risk2000entry.tmp
echo "SELECT DATE_FORMAT(ll.gbetl_datetime,'%Y%m01') yyyymm01, COUNT(1) c, SUM(G_QTY) s, SUM(DECL_TOTAL) ts, CODE_TS AS h_s_code,ORIGIN_COUNTRY AS country FROM riskh2000_extr.entry_list ll JOIN riskh2000_extr.entry_head hh ON ll.entry_id = hh.entry_id WHERE hh.trade_mode='0110' AND hh.I_E_FLAG='E' GROUP BY h_s_code,yyyymm01,country
" | ./gbase_sql.sh > $PWD/export_ee_yyyymm01_cty_risk2000entry_0110e.tmp

#mysql --host=127.0.0.1 --port=3306 --user=root --password=szu -e "load data local infile '$PWD/export_ee_yyyymm01_cty_risk2000entry.tmp' replace into table dba.rpt_ee_yyyymm_code_country_risk2000entry ignore 1 lines (yyyymm01,c,s,ts,h_s_code,country) ;"
mysql --host=127.0.0.1 --port=3306 --user=root --password=szu -e "load data local infile '$PWD/export_ee_yyyymm01_cty_risk2000entry_0110e.tmp' replace into table dba.rpt_ee_yyyymm_code_country_risk2000entry_0110e ignore 1 lines (yyyymm01,c,s,ts,h_s_code,country) ;"

# step 2: calc local
# cat dba_rpt_rank_ee_risk2000entry.sql | ./mysql3306.sh dba

