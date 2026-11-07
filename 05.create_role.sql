==============
--use database and chema
==============
use database HOTEL_DATABASE;
use schema dev;

select current_role();

use role accountadmin;

==============
--Create a use
==============
create user user_02
password = 'test@1234'
comment = 'User for testing purpose'
must_change_password = false;
=============================
--Login to above user_02 check the below
=======================
select current_role();
show grants to role_public;

create database test_database;

desc user user_02;
show grants to user user_02;
show grants on user user_02;
===============================
--Create another user
===============================
create user user_03 
    password = "test@1234" 
    default_role = "SYSADMIN" 
    comment = 'User3 for testing purpose'
    must_change_password = false;
GRANT ROLE "SYSADMIN" TO USER user_03;

===============================
--adding more roles to user02 & USER_03 then refresh the user_02 account see the results
===============================
GRANT ROLE "SECURITYADMIN" TO USER user_03;
GRANT ROLE "USERADMIN" TO USER user_03;

