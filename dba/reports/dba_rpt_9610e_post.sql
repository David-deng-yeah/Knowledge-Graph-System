use dba;
-- rank by country
DROP TABLE IF EXISTS dba_rpt_9610e_cty;
CREATE TABLE dba_rpt_9610e_cty
SELECT v.*,IF(@p =`年月`,@rk :=@rk+1,IF(@p :=`年月`,@rk:=1,0)) cty_rank FROM 
(
SELECT yyyy as `年月`,`COUN_C_NAME` as `国家`, `cty` as `国家码`,
SUM(`ts`)总价总和,SUM(`c`)业务单数总和,SUM(`s`)数量总和
FROM `dba_rpt_9610e` `rr`
   JOIN `country` `cc` ON ((`rr`.`cty` = `cc`.`COUNTRY_CODE`))
WHERE rr.`trade_mode`='9610' AND flg='E'
GROUP BY `年月`,`国家`,`国家码` 
ORDER BY `年月`,`总价总和` DESC
) v, (SELECT @rk :=0, @p :=NULL) r;

ALTER TABLE dba_rpt_9610e_cty ADD INDEX idx_yyyymm_cty (`年月`,`国家`);

-- rank by country/code4
DROP TABLE IF EXISTS dba_rpt_9610e_code4;
CREATE TABLE dba_rpt_9610e_code4
SELECT v2.*,IF(@p =CONCAT(`年月`,`国家`),@rk :=@rk+1,IF(@p :=CONCAT(`年月`,`国家`),@rk:=1,0)) g_rank FROM 
(
SELECT yyyy as `年月`,`COUN_C_NAME` as `国家`, `cty` as `国家码`, `code_4` as `编码四位`,gg.good_name as `编码名四`,
    SUM(`ts`)总价总和,SUM(`c`)业务单数总和,SUM(`s`)数量总和
FROM `dba_rpt_9610e` `rr`
    JOIN `country` `cc` ON `rr`.`cty` = `cc`.`COUNTRY_CODE`
    JOIN `good_code_name` `gg` ON `rr`.`code_4` = `gg`.`good_code`
WHERE rr.`trade_mode`='9610' AND flg='E'
GROUP BY `年月`,`国家`,`国家码`,`编码四位`,`编码名四`
ORDER BY `年月`,`国家`,`总价总和` DESC
) v2, (SELECT @rk :=0, @p :=NULL) r2;

ALTER TABLE dba_rpt_9610e_code4 ADD INDEX idx_yyyymm_cty (`年月`,`国家`);

-- rank by country/code
DROP TABLE IF EXISTS dba_rpt_9610e_code;
CREATE TABLE dba_rpt_9610e_code
SELECT v2.*,IF(@p =CONCAT(`年月`,`国家`),@rk :=@rk+1,IF(@p :=CONCAT(`年月`,`国家`),@rk:=1,0)) g_rank FROM
(
SELECT yyyy AS `年月`,`COUN_C_NAME` AS `国家`, `cty` AS `国家码`, `code` AS `编码`,
SUM(`ts`)总价总和,SUM(`c`)业务单数总和,SUM(`s`)数量总和
FROM (`dba_rpt_9610e` `rr`
  JOIN `country` `cc` ON `rr`.`cty` = `cc`.`COUNTRY_CODE`)
WHERE rr.`trade_mode`='9610' AND flg='E'
GROUP BY `年月`,`国家`,`国家码`,`编码`
ORDER BY `年月`,`国家`,`总价总和` DESC
) v2, (SELECT @rk :=0, @p :=NULL) r2;

ALTER TABLE dba_rpt_9610e_code ADD INDEX idx_yyyymm_cty (`年月`,`国家`);
