CREATE TABLE Movie (
  id INT,
  title VARCHAR(100),
  year INT,
  rating VARCHAR(100),
  company VARCHAR(50),
  PRIMARY KEY (id)
);

CREATE TABLE Actor(
	id INT,
	last VARCHAR(20),
	first VARCHAR(20),
	sex VARCHAR(6),
	dob DATE,
	dod DATE,
	PRIMARY KEY (id)
);


CREATE TABLE Director(
	id INT,
	last VARCHAR(20),
	first VARCHAR(20),
	dob DATE,
	dod DATE,
	PRIMARY KEY (id)
);

CREATE TABLE MovieGenre(
	mid INT,
	genre VARCHAR(20),
	PRIMARY KEY (mid, genre)
);

CREATE TABLE MovieDirector(
	mid INT,
	did INT,
	PRIMARY KEY(mid)
);

CREATE TABLE MovieActor(
	mid INT,
	aid INT,
	role VARCHAR(50),
	PRIMARY KEY (mid,aid)
);

CREATE TABLE Review(
	name VARCHAR(20),
	time TIMESTAMP,
	mid INT,
	rating INT,
	comment VARCHAR(500),
	PRIMARY KEY (name, mid)
);

CREATE TABLE MaxPersonID(
	id INT
);

CREATE TABLE MaxMovieID(
	id INT
);


