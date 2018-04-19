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

SELECT Director.first, Director.last as genres
FROM Director
INNER JOIN MovieDirector ON Director.id = MovieDirector.did
INNER JOIN MovieGenre ON MovieDirector.mid = MovieGenre.mid
WHERE MovieGenre.genre = "Romance"
GROUP BY MovieGenre.mid;