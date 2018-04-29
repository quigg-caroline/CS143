DROP DATABASE IF EXISTS hw2;
CREATE DATABASE hw2;
USE hw2;

-- Data for part 1.

DROP TABLE IF EXISTS caltrans;
CREATE TABLE `caltrans` (
  `reported` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `highway` varchar(6) NOT NULL,
  `area` varchar(255) NOT NULL,
  `text` text NOT NULL,
  `hash` varchar(32) NOT NULL,
  PRIMARY KEY (reported, highway, area, hash)
);

LOAD DATA LOCAL INFILE 'caltrans.csv' INTO TABLE caltrans FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- Data for part 3.
-- For simplicity, this does not match HW 1 intentionally.
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS trip_starts;
DROP TABLE IF EXISTS trip_ends;
CREATE TABLE user (
	user_id MEDIUMINT PRIMARY KEY,
	ccnumber VARCHAR(19),
	expiration TIMESTAMP,
	email VARCHAR(255)
) ENGINE=InnoDB;
CREATE TABLE trip_starts (  -- 2 3 4  1  5 6
	trip_id INT PRIMARY KEY,
	user_id MEDIUMINT,
	scooter_id SMALLINT,
	time TIMESTAMP,
	lon DECIMAL(8,6),
	lat DECIMAL(8,6)
)ENGINE=InnoDB;
CREATE TABLE trip_ends (
	trip_id INT PRIMARY KEY,
	user_id MEDIUMINT,
	scooter_id SMALLINT,
	time TIMESTAMP,
	lon DECIMAL(8,6),
	lat DECIMAL(8,6)
)ENGINE=InnoDB;

LOAD DATA LOCAL INFILE 'trip_starts.csv' INTO TABLE trip_starts FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'trip_ends.csv' INTO TABLE trip_ends FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'users.csv' INTO TABLE user FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
