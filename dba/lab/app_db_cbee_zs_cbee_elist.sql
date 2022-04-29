DROP SERVER IF EXISTS server_db_cbee_zs;
CREATE SERVER 'server_db_cbee_zs' FOREIGN DATA WRAPPER mysql OPTIONS (HOST '10.54.202.211', PORT 5258, USER 'app_gbase_zhjj', PASSWORD 'drawer@#$0427', DATABASE 'app_db_cbee_zs');

CREATE TABLE `app_db_cbee_zs_cbee_elist` (
  `ID` VARCHAR(64) DEFAULT NULL,
  `CO_EL_NO` VARCHAR(32) DEFAULT NULL,
  `PRE_NO` VARCHAR(64) DEFAULT NULL,
  `EMS_NO` VARCHAR(32) DEFAULT NULL,
  `ORDER_NO` VARCHAR(64) DEFAULT NULL,
  `EBP_CODE` VARCHAR(32) DEFAULT NULL,
  `EBP_NAME` VARCHAR(300) DEFAULT NULL,
  `EBC_CODE` VARCHAR(32) DEFAULT NULL,
  `EBC_NAME` VARCHAR(300) DEFAULT NULL,
  `LOGISTICS_NO` VARCHAR(64) DEFAULT NULL,
  `LOGISTICS_CODE` VARCHAR(32) DEFAULT NULL,
  `LOGISTICS_NAME` VARCHAR(300) DEFAULT NULL,
  `INVT_NO` VARCHAR(32) DEFAULT NULL,
  `I_E_FLAG` VARCHAR(4) DEFAULT NULL,
  `DECL_TIME` DATETIME DEFAULT NULL,
  `CUSTOMS_CODE` VARCHAR(32) DEFAULT NULL,
  `PORT_CODE` VARCHAR(8) DEFAULT NULL,
  `I_E_DATE` DATETIME DEFAULT NULL,
  `AGENT_CODE` VARCHAR(32) DEFAULT NULL,
  `AGENT_NAME` VARCHAR(300) DEFAULT NULL,
  `AREA_CODE` VARCHAR(32) DEFAULT NULL,
  `AREA_NAME` VARCHAR(300) DEFAULT NULL,
  `TRADE_MODE` VARCHAR(8) DEFAULT NULL,
  `TRAF_MODE` VARCHAR(4) DEFAULT NULL,
  `TRAF_NAME` VARCHAR(100) DEFAULT NULL,
  `VOYAGE_NO` VARCHAR(32) DEFAULT NULL,
  `BILL_NO` VARCHAR(60) DEFAULT NULL,
  `LOCT_NO` VARCHAR(32) DEFAULT NULL,
  `LICENSE_NO` VARCHAR(32) DEFAULT NULL,
  `COUNTRY` VARCHAR(6) DEFAULT NULL,
  `FREIGHT` DECIMAL(19,5) DEFAULT NULL,
  `INSURED_FEE` DECIMAL(19,5) DEFAULT NULL,
  `CURRENCY` VARCHAR(6) DEFAULT NULL,
  `WRAP_TYPE` VARCHAR(2) DEFAULT NULL,
  `PACK_NO` INT(11) DEFAULT NULL,
  `GROSS_WEIGHT` DECIMAL(19,5) DEFAULT NULL,
  `NET_WEIGHT` DECIMAL(19,5) DEFAULT NULL,
  `NOTE` VARCHAR(2000) DEFAULT NULL,
  `GUID` VARCHAR(64) DEFAULT NULL,
  `APP_TYPE` VARCHAR(4) DEFAULT NULL,
  `APP_TIME` DATETIME DEFAULT NULL,
  `APP_SENDER_ID` VARCHAR(100) DEFAULT NULL,
  `CREATE_DATE` DATETIME DEFAULT NULL,
  `DISTRICT_CUSTOMS` VARCHAR(8) DEFAULT NULL,
  `TOTAL_PRICE` DECIMAL(19,5) DEFAULT NULL,
  `INSPECTION_STATUS` BIGINT(20) DEFAULT NULL,
  `RISK_INFO` VARCHAR(2000) DEFAULT NULL,
  `TOTAL_PACKAGE_NO` VARCHAR(64) DEFAULT NULL,
  `POD` VARCHAR(4) DEFAULT NULL,
  `F_FLAG` VARCHAR(4) DEFAULT NULL,
  `F_CURRENCY` VARCHAR(4) DEFAULT NULL,
  `I_CURRENCY` VARCHAR(4) DEFAULT NULL,
  `I_FLAG` VARCHAR(4) DEFAULT NULL,
  `STATISTICS_FLAG` VARCHAR(4) DEFAULT NULL,
  `NORMAL_STATUS` VARCHAR(1) DEFAULT NULL,
  `TOTAL_PRICE_RMB` DECIMAL(19,5) DEFAULT NULL,
  `FREIGHT_RMB` DECIMAL(19,5) DEFAULT NULL,
  `INSURED_FEE_RMB` DECIMAL(19,5) DEFAULT NULL,
  `VALUE_RATE` DECIMAL(19,5) DEFAULT NULL,
  `LAST_MODIFY_DATE` DATETIME DEFAULT NULL,
  `LAST_MODIFY_CODE` VARCHAR(16) DEFAULT NULL,
  `LAST_MODIFY_USER` VARCHAR(100) DEFAULT NULL,
  `LAST_MODIFY_USER_FULL_PATH` VARCHAR(300) DEFAULT NULL,
  `LAST_MODIFY_DESC` VARCHAR(1000) DEFAULT NULL,
  `LOCK_USER` VARCHAR(255) DEFAULT NULL,
  `LOCK_TIME` DATETIME DEFAULT NULL,
  `LOCK_NODE` VARCHAR(255) DEFAULT NULL,
  `USD_RATE` DECIMAL(19,5) DEFAULT NULL,
  `OWNER_CODE` VARCHAR(32) DEFAULT NULL,
  `OWNER_NAME` VARCHAR(255) DEFAULT NULL,
  `COMPARISON_WAY` VARCHAR(2) DEFAULT NULL,
  `ARRIVAL_TIME` DATETIME DEFAULT NULL,
  `BIND_TYPE` VARCHAR(1) DEFAULT NULL,
  `EBP_SCC_CODE` VARCHAR(32) DEFAULT NULL,
  `EBC_SCC_CODE` VARCHAR(32) DEFAULT NULL,
  `LOGISTICS_SCC_CODE` VARCHAR(32) DEFAULT NULL,
  `AGENT_SCC_CODE` VARCHAR(32) DEFAULT NULL,
  `AREA_SCC_CODE` VARCHAR(32) DEFAULT NULL,
  `GOODS_INFO` VARCHAR(3000) DEFAULT NULL,
  `OWNER_SCC_CODE` VARCHAR(32) DEFAULT NULL,
  `gbetl_datetime` VARCHAR(32) DEFAULT NULL
)
ENGINE=FEDERATED CONNECTION='server_db_cbee_zs/cbee_elist' DEFAULT CHARSET=utf8mb4;

