<html>
<body>

<link rel="stylesheet" href="styling.css">
<?php include('navigation.php') ?>

<div class = "header" >Actor Information Page</div>
	<?php
		$get_string =  $_SERVER['QUERY_STRING'];
		parse_str($get_string, $get_array);

		//query actor info
		echo "<div>";
		echo "<h3> Actor Information is: </h3>";
		$query_string = "SELECT first, last, sex, dob, dob FROM Actor WHERE id=".$get_array['id'];
		 $db = new mysqli('localhost', 'cs143', '', 'TEST');

	      if ($db->connect_errno > 0){
	        die('Unable to connect to database');
	      }

	    $result = $db->query($query_string);
	 	$result_arr = $result -> fetch_assoc();

	 	echo "<table border=1>";
	 	echo "<tr>" ;
	 	echo "<th> Name </th> <th> Sex </th> <th> Date of Birth </th> <th> Date of Death </th>";
	 	echo "</tr>";

	 	echo "<tr>";
	 	//add name
	 	echo "<td>".$result_arr['first']." ".$result_arr['last']."</td>";
	 	//add sex
	 	echo "<td>".$result_arr['sex']." "."</td>";
	 	//add dob
	 	echo "<td>".$result_arr['dob']."</td>";
	 	//add dod if possible
	 	if (empty($result_arr['dod']))
	 	{
	 		echo "<td> Still Alive </td>";
	 	}
	 	else
	 	{
	 		echo "<td>".$result_arr['dod']."</td>";
	 	}
	 	echo "</table>";
	 	echo "</div>";

	 	//get movie info
	 	echo "<h3>Actor Movie Roles</h3>";
	 	$query_string = 
	 		"SELECT MovieActor.role, Movie.title, Movie.id FROM MovieActor
	 		INNER JOIN Movie ON MovieActor.mid=Movie.id
	 		WHERE MovieActor.aid=".$get_array['id'];

	 	$result = $db->query($query_string);

	 	echo "<table border=1>";
	 	echo "<tr>" ;
	 	echo "<th> Role </th> <th> Movie </th>";
	 	echo "</tr>";
	 	while($result_arr = $result -> fetch_assoc())
	 	{
	 		echo "<tr><td>". $result_arr['role'].
	 			"</td><td><a href = \"show-movie.php?id=".$result_arr['id']."\">"
	 			.$result_arr['title']."</a></td></tr>";
	 	}
	 	echo "</table>";




	?>
</body>
</html>