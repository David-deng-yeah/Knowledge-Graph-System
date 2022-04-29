SELECT tt.*, cc.rank AS cty_rank,cn.`good_name` AS `code_name`
FROM dba_rpt_risk2000entry_cty cc
 JOIN dba_rpt_risk2000entry_code tt ON cc.`年月`=tt.`年月` AND cc.`国家` = tt.`国家`
 LEFT JOIN good_code_name cn ON tt.`编码` = cn.`good_code`
WHERE cc.rank<10 AND tt.rank<10


