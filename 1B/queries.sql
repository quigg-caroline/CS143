SELECT Actor.first, Actor.last
FROM Actor
INNER JOIN MovieActor ON Actor.id = MovieActor.aid
INNER JOIN Movie ON MovieActor.mid = Movie.id
WHERE Movie.title = 'Die Another Day';

SELECT COUNT(*)
FROM (
  SELECT aid, COUNT(*) as count FROM MovieActor GROUP BY aid
  HAVING count > 1
) A1;




SELECT mid, COUNT(*) as count FROM MovieGenre GROUP BY mid
HAVING genre = "Romance" AND genre = "Comedy";

-- WHERE A.mid = B.mid AND A.genre <> B.genre;

SELECT Director.first, Director.last, MovieDirector.mid, GROUP_CONCAT(MovieGenre.genre) as genres
FROM Director
INNER JOIN MovieDirector ON Director.id = MovieDirector.did
INNER JOIN MovieGenre ON MovieDirector.mid = MovieGenre.mid
WHERE MovieGenre.genre = "Romance" OR MovieGenre.genre = "Comedy"
GROUP BY MovieGenre.mid;
-- GROUP BY MovieGenre.mid;

SELECT genre
FROM MovieGenre
WHERE mid = 4536;
