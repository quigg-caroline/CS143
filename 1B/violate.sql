-- This violates the movie primary key, it is not unique
INSERT INTO Movie
VALUES (173, 'Shes NOT the Man', 1960, 'PG-13', 'Disney');

--This violates the actor primary key, it is not unique
INSERT INTO Actor 
VALUES (64, 'Quigg', 'Christina', 'FEMALE', 19970208, NULL);

--This violates the actor check that ensures death comes AFTER birth
INSERT INTO Actor 
VALUES (68637, 'Quigg', 'Caroline', 'FEMALE', 19970208, 19950721);

--This violates the actor primary key, it is not unique
INSERT INTO Director
VALUES (3141, 'Obama', 'Malia', 19960908, NULL);

--This violates the director check, directors should have been born
INSERT INTO Director
VALUES (68627, 'The Rapper', 'Chance', NULL, NULL);

--This violates the MovieGenre foreign key because there is an entry in MovieGenre for a movie that doesn't exist
INSERT INTO MovieGenre
VALUES (5000, 'Romance');

--This violates the MovieDirector foreign key because there is an entry in MovieDirector for a movie that doesn't exist
INSERT INTO MovieDirector
VALUES (70000, 500);

--This violates the MovieDirector foreign key because there is an entry in MovieDirector for a director that doesn't exist
INSERT INTO MovieDirector
VALUES (74, 70000);

--This violates the MovieActor foreign key because there is an entry in MovieActor for a movie that doesn't exist
INSERT INTO MovieActor
VALUES (70000, 31);

--This violates the MovieActor foreign key because there is an entry in MovieActor for a actor that doesn't exist
INSERT INTO MovieActor
VALUES (74, 70000);

--This violates the Review foreign key because there is an entry in Review for a movie that doesn't exist
INSERT INTO MovieActor
VALUES ('Han Solo', '2018-01-05 18:00:00', 70000, 4, 'cool movie bro');

--This violates the Review check because the rating cannot be negative
INSERT INTO MovieActor
VALUES ('Chewie', '2018-02-05 19:20:00', 74, -4, 'movie sucked bro');

