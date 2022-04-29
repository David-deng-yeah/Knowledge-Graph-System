DROP TABLE IF EXISTS rpt_rank_ee_yyyy_country;
CREATE TABLE rpt_rank_ee_yyyy_country
SELECT v.*,IF(@p =`年月`,@rk :=@rk+1,IF(@p :=`年月`,@rk:=1,0)) rank FROM 
(
SELECT `年月`,`国家`,`国家码`,SUM(`总价`)总价总和,SUM(`业务单数`)业务单数总和,SUM(`数量`)数量总和
FROM v_ee_yyyymm_code4_cty
GROUP BY `年月`,`国家`,`国家码` 
ORDER BY `年月`,`总价总和` DESC
) v, (SELECT @rk :=0, @p :=NULL) r;

ALTER TABLE rpt_rank_ee_yyyy_country ADD INDEX idx_yyyymm_cty (`年月`,`国家`);

DROP TABLE IF EXISTS rpt_rank_ee_yyyy_country_code4;
CREATE TABLE rpt_rank_ee_yyyy_country_code4
SELECT v2.*,IF(@p =CONCAT(`年月`,`国家`),@rk :=@rk+1,IF(@p :=CONCAT(`年月`,`国家`),@rk:=1,0)) rank FROM 
(
SELECT `年月`,`国家`,`国家码`,`编码四位` ,SUM(`总价`)总价总和,SUM(`业务单数`)业务单数总和,SUM(`数量`)数量总和
FROM v_ee_yyyymm_code4_cty
GROUP BY `年月`,`国家`,`国家码`,`编码四位` 
ORDER BY `年月`,`国家`,`总价总和` DESC
) v2, (SELECT @rk :=0, @p :=NULL) r2;

ALTER TABLE rpt_rank_ee_yyyy_country_code4 ADD INDEX idx_yyyymm_cty (`年月`,`国家`);

DROP TABLE IF EXISTS rpt_rank_ee_yyyy_country_code4_top10x10;
CREATE TABLE rpt_rank_ee_yyyy_country_code4_top10x10
SELECT tt1.*,tt2.`类别编码`,tt2.`类别rank`,tt2.`类别总价总和` 
FROM (
SELECT t1.`年月`,t1.`国家`,t1.rank 国家rank,t1.`总价总和` `国家总价总和`
FROM rpt_rank_ee_yyyy_country t1
WHERE rank<=10
) tt1
JOIN (
SELECT t2.`年月`,t2.`国家`,t2.`编码四位` 类别编码, t2.rank 类别rank,t2.`总价总和` `类别总价总和`
FROM rpt_rank_ee_yyyy_country_code4 t2
WHERE rank<=10
) tt2
ON tt1.`年月`=tt2.`年月` AND tt1.`国家`=tt2.`国家`;
ALTER TABLE rpt_rank_ee_yyyy_country_code4_top10x10 ADD INDEX idx_yyyymm_cty (`年月`,`国家`);

DROP TABLE IF EXISTS rpt_rank_ee_yyyy_country_code4_top10x100;
CREATE TABLE rpt_rank_ee_yyyy_country_code4_top10x100
SELECT tt1.*,tt2.`类别编码`,tt2.`类别rank`,tt2.`类别总价总和` 
FROM (
SELECT t1.`年月`,t1.`国家`,t1.rank 国家rank,t1.`总价总和` `国家总价总和`
FROM rpt_rank_ee_yyyy_country t1
WHERE rank<=10
) tt1
JOIN (
SELECT t2.`年月`,t2.`国家`,t2.`编码四位` 类别编码, t2.rank 类别rank,t2.`总价总和` `类别总价总和`
FROM rpt_rank_ee_yyyy_country_code4 t2
WHERE rank<=100
) tt2
ON tt1.`年月`=tt2.`年月` AND tt1.`国家`=tt2.`国家`;
ALTER TABLE rpt_rank_ee_yyyy_country_code4_top10x100 ADD INDEX idx_yyyymm_cty (`年月`,`国家`);
