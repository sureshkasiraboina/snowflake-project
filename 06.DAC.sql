=====================
--Context Function
====================
select current_account(), current_user(), current_role();

=====================
--List all the users and ownership
====================
use role accountadmin;
use role sysadmin;
show users;

=====================
--Create database and table in sysadmin role and see if user02 can see it or not
====================
USE ROLE SYSADMIN;
CREATE DATABASE TEST_DAC_DB;
CREATE SCHEMA TEST_DAC_SCHEMA;
SHOW SCHEMAS;
SHOW DATABASES;
CREATE TABLE TEST_TABLE (ID INT, NAME VARCHAR(50));
SHOW TABLES;

=======================
--HEAD OVER TO THE USER02 AND SEE AND DO SOME ACTION
========================
=============
--CREATE OR DELETE TABLE TO SEE IF IT WORKS
=============
use role sysadmin;
USE DATABASE TEST_DATABASE;
USE SCHEMA TEST_DAC_DB.TEST_DAC_SCHEMA;

CREATE TABLE TEST_DAC_USER02(NAME VARCHAR);
DROP TABLE TEST_TABLE; -- CREATED THIS TABLE IN OWNER ACCOUNT
=========================



