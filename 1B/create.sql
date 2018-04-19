CREATE TABLE Movie (
  id INT,
  title VARCHAR(100),
  year INT,
  rating VARCHAR(100),
  company VARCHAR(50),
  PRIMARY KEY (id)
	-- Movie id should be unique
);

CREATE TABLE Actor(
	id INT,
	last VARCHAR(20),
	first VARCHAR(20),
	sex VARCHAR(6),
	dob DATE,
	dod DATE,
	PRIMARY KEY (id),
	-- Actor id should be unique
	CHECK (dod IS NULL OR YEAR(dod) > YEAR(dob))
	-- Actor's death year should be after his/her birth year (or the actor isn't dead yet)
);


CREATE TABLE Director(
	id INT,
	last VARCHAR(20),
	first VARCHAR(20),
	dob DATE,
	dod DATE,
	PRIMARY KEY (id),
	-- Director id should be unique
	CHECK (dob IS NOT NULL)
	-- Director must have been born
);

CREATE TABLE MovieGenre(
	mid INT,
	genre VARCHAR(20),
	PRIMARY KEY (mid, genre),
	-- Every row should be unique (movie genre pairing)
	FOREIGN KEY (mid) REFERENCES Movie(id)
	-- More information on the movie through the movie id
) ;

CREATE TABLE MovieDirector(
	mid INT,
	did INT,
	PRIMARY KEY(mid),
	FOREIGN KEY (mid) REFERENCES Movie(id),
	-- More information on the movie through the movie id
	FOREIGN KEY (did) REFERENCES Director(id)
	-- More information on the director through the director id
) ;

CREATE TABLE MovieActor(
	mid INT,
	aid INT,
	role VARCHAR(50),
	PRIMARY KEY (mid,aid),
	-- Every row should be unique (movie actor pairing)
	FOREIGN KEY (mid) REFERENCES Movie(id),
	-- More information on the movie through the movie id
	FOREIGN KEY (aid) REFERENCES Actor(id)
	-- More information on the actor through the actor id
) ;

CREATE TABLE Review(
	name VARCHAR(20),
	time TIMESTAMP,
	mid INT,
	rating INT,
	comment VARCHAR(500),
	FOREIGN KEY (mid) REFERENCES Movie(id),
	-- More information on the movie through the movie id
	CHECK (rating >= 0)
	-- Rating cannot be negative
) ;

CREATE TABLE MaxPersonID(
	id INT
);

CREATE TABLE MaxMovieID(
	id INT
);


