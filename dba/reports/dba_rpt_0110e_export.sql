SELECT
  DATE_FORMAT (ll.gbetl_datetime, '%Y0101') yyyy,
  COUNT (1) c, -- order count
  SUM (G_QTY) s, -- quantity sum
  SUM (DECL_TOTAL) ts, -- total amount
  CODE_TS AS `code`, -- code of the good
  ORIGIN_COUNTRY AS cty, -- country 
  I_E_FLAG AS flg, -- the I/E flag
  trade_mode 
FROM riskh2000_extr.entry_list ll JOIN riskh2000_extr.entry_head hh ON ll.entry_id = hh.entry_id
WHERE trade_mode = '0110' and I_E_FLAG='E'
GROUP BY `code`, yyyy, cty, trade_mode, I_E_FLAG
;
