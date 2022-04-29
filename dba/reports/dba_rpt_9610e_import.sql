use dba;
drop table IF EXISTS dba.dba_rpt_9610e;
CREATE TABLE `dba_rpt_9610e` (
  `yyyy` date NOT NULL,
  `c` int(11) DEFAULT NULL,
  `s` bigint(20) DEFAULT NULL,
  `ts` bigint(20) DEFAULT NULL,
  `code` varchar(16) NOT NULL,
  `cty` int(11) NOT NULL,
  `flg` varchar(1) NOT NULL,
  `trade_mode` varchar(4) NOT NULL,
  `code_4` varchar(5) GENERATED ALWAYS AS (substr(`code`,1,4)) VIRTUAL,
  PRIMARY KEY (`yyyy`,`code`,`cty`,`flg`,`trade_mode`),
  KEY `idx_code` (`code`),
  KEY `idx_cty` (`cty`),
  KEY `idx_yyyy` (`yyyy`),
  KEY `idx_flg` (`flg`),
  KEY `idx_trade_mode` (`trade_mode`),
  KEY `idx_code_4` (`code_4`(4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
load data local infile 'dba_rpt_9610e.tmp'
replace into table dba.dba_rpt_9610e
ignore 1 lines (yyyy,c,s,ts,code,cty,flg,trade_mode);
