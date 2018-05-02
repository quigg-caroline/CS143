<html>
<body>

<link rel="stylesheet" href="styling.css">
<?php include('navigation.php') ?>
		<div class = "header" >Search Movie & Actor Info</div>
	<form class = "nope" method = "post" action="search.php" >
		<div>
			<input type="text" name="search">
		</div>
		<button type = "submit" name = "submit" >Search</button>
	</form>
	<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {
    	$search = $_POST['search'];
    	$search_words = explode(" ", $search);
    	//check input is ok

    	//search actors & movies using the search
    	$query_actor= "SELECT name,last, id,dob FROM 
    	(SELECT CONCAT(first, \" \",last) as name,last, id,dob FROM
    		Actor)temp
		WHERE ";

		//iterate over words to search for and conca
		foreach ($search_words as $word) {
			if($word === end($search_words))
			{
				$query_actor.="name LIKE \"%".$word."%\"";
			}
			else{
				$query_actor.="name LIKE \"%".$word."%\" AND ";		
			}

		}

		//show actor info
		$query_actor.= " ORDER BY last ASC";
		$db = new mysqli('localhost', 'cs143', '', 'CS143');

	      if ($db->connect_errno > 0){
	        die('Unable to connect to database');
	      }
	     $result = $db->query($query_actor);
	     if($result===FALSE)
	     {
	     	exit( "Error: " . $query_actor . "<br>" . $db->error);
	     }

	    echo "<h2>Actors</h2>";
	    echo "<table border=1>";
	 	echo "<tr>" ;
	 	echo "<th> Actor </th> <th> Date of Birth </th>";
	 	echo "</tr>";
	 	while($result_arr = $result -> fetch_assoc())
	 	{
	 		echo "<tr>".
	 			"<td><a href = \"show-actor.php?id=".$result_arr['id']."\">"
	 			.$result_arr['name']."</a></td>"
	 			."<td>".$result_arr['dob']
	 			."</td></tr>";
	 	}
	 	echo "</table>";

	 	//show movie info
	 	$query_movie = "SELECT title,year,id FROM Movie
		WHERE ";
		foreach ($search_words as $word) {
			if($word === end($search_words))
			{
				$query_movie.="title LIKE \"%".$word."%\"";
			}
			else{
				$query_movie.="title LIKE \"%".$word."%\" AND ";		
			}
		}
		$query_movie.= " ORDER BY title ASC";	

		 $result = $db->query($query_movie);
	     if($result===FALSE)
	     {
	     	exit("Error: " . $query_movie . "<br>" . $db->error);
	     }


	    echo "<h2>Movies</h2>";		
	    echo "<table border=1>";
	 	echo "<tr>" ;
	 	echo "<th> Title</th> <th> Year</th>";
	 	echo "</tr>";
	 	while($result_arr = $result -> fetch_assoc())
	 	{
	 			echo "<tr>".
	 			"<td><a href = \"show-movie.php?id=".$result_arr['id']."\">"
	 			.$result_arr['title']."</a></td>"
	 			."<td>".$result_arr['year']
	 			."</td></tr>";
	 	}
	 	echo "</table>";

}}
    ?>
</body>
</html>
