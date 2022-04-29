drop server if exists server_gbase_inforschema;
create server 'server_gbase_inforschema'
foreign data wrapper mysql options
(host '10.54.202.211', port 5258, user 'app_gbase_zhjj', password 'drawer@#$0427', database 'information_schema');
