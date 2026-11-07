-----Create DATABASE-----
create database media;
create schema analytics;

-----USE DATABASE-------
use database media;
use schema analytics;

--Create File Format---

CREATE OR REPLACE FILE FORMAT MEDIA.ANALYTICS.CSV_FORMAT
TYPE = CSV
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
DATE_FORMAT = 'DD-MM-YYYY'
NULL_IF = ('NULL','N/A','');