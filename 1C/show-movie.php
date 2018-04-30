<html>
<body>
	<h2>Movie Information Page</h2>
	<?php
		$get_string =  $_SERVER['QUERY_STRING'];
		parse_str($get_string, $get_array);
		echo "<h3>Movie Info</h3>";

		//get movie information
		$db = new mysqli('localhost', 'cs143', '', 'TEST');

	      if ($db->connect_errno > 0){
	        die('Unable to connect to database');
	      }

	     $query_movie = "SELECT Movie.title, Movie.company, Movie.rating,
	     	CONCAT(Director.first,\" \", Director.last) as director,
	     	Movie.year,
	     	MovieGenre.genre FROM Movie
	     	INNER JOIN MovieDirector ON MovieDirector.mid = Movie.id
	     	INNER JOIN Director ON MovieDirector.did = Director.id
	     	INNER JOIN MovieGenre ON Movie.id=MovieGenre.mid
	     	WHERE Movie.id=".$get_array['id'];
	    $result = $db->query($query_movie);
	    if ($result === FALSE)
	    {
	    	exit ("Error: " . $query_movie . "<br>" . $db->error);
	    }
	    $result_arr = $result -> fetch_assoc();
	    echo "<table>";

	 	echo "<tr>"; 
	 	echo "<td> Title: ".$result_arr['title']."(".$result_arr['year'].")</td>";
	 	echo "</tr>";

	 	echo "<tr>"; 
	 	echo "<td> Producer: ".$result_arr['company']."</td>";
	 	echo "</tr>";

	 	echo "<tr>"; 
	 	echo "<td> MPAA Rating: ".$result_arr['rating']."</td>";
	 	echo "</tr>";

	 	echo "<tr>"; 
	 	echo "<td> Director: ".$result_arr['director']. "</td>";
	 	echo "</tr>";
	 	//show all the genres
	 	echo "<tr><td> Genre: ".$result_arr['genre']. " ";
	 	while($result_arr = $result -> fetch_assoc())
	 	{
	 		echo $result_arr['genre']. " ";
	 	}
	 	echo"</td>";
	 	echo "</tr>";
	 	echo "</table>";

		//show actor information
		$query_actors = "SELECT CONCAT(Actor.first,\" \",Actor.last) as name,
			MovieActor.role, Actor.id FROM Actor INNER JOIN MovieActor
			ON MovieActor.aid = Actor.id WHERE MovieActor.mid=".$get_array['id'];
		$result = $db->query($query_actors);
		echo "<h3>Actors in Movie: </h3>";
		echo "<table border=1>";
	 	echo "<tr>" ;
	 	echo "<th> Role </th> <th> Actor </th>";
	 	echo "</tr>";
	 	while($result_arr = $result -> fetch_assoc())
	 	{
	 		echo "<tr><td>". $result_arr['role'].
	 			"</td><td><a href = \"show-actor.php?id=".$result_arr['id']."\">"
	 			.$result_arr['name']."</a></td></tr>";
	 	}
	 	echo "</table>";

	 	//show rating information

	 	echo "<h3>Audience Ratings</h3>";
	 	$query_review = "SELECT COUNT(rating) as total, AVG(rating) as avg FROM Review
	 		WHERE mid=" .$get_array['id'];
	 	$result = $db->query($query_review);
	 	if( $result === FALSE)
	    {
	    	exit ("Error: " . $query_review . "<br>" . $db->error);
	    }
	    $result_arr = $result -> fetch_assoc();
	    if ($result_arr['total'] < 1)
	    {
	    	echo "No reviews yet";
	    	echo "</br>";
	    }
	    else
	    {
	    	echo "Out of the ".$result_arr['total']." reviews, the average rating for this
	    	movie is ".number_format($result_arr['avg'],2). "/5";
	    	echo "</br>";
	    }
	 	echo "<a href=\"add-review.php\" >Add your review</a>";

	 	//get reviews
	 	echo "<h3>What people are saying about this movie:</h3>";
	 	$query_review = "SELECT * FROM Review
	 		WHERE mid=" .$get_array['id'];
	 	$result = $db->query($query_review);
	 	if( $result === FALSE)
	    {
	    	exit ("Error: " . $query_review . "<br>" . $db->error);
	    }

	    echo "<table>";
	 	while($result_arr = $result -> fetch_assoc())
	 	{
	 		echo "<tr>";
	 		echo "<td>".$result_arr['name']." rated this movie ".$result_arr['rating'].
	 			" our of 5 stars.</td>";
	 		echo "</tr>";
	 		echo "<tr>";
	 		echo "<td> \"".$result_arr['comment']. "\"";
	 		echo "</td></tr>";
	 	}
	 	echo "</table>";

	?>
</body>
</html>