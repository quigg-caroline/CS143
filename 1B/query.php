<html>

<body>
<h2>PHP SQL Query Interface</h2>
Enter a SQL query into the box to query the database </br>


<form method="post" action="<?php echo $_SERVER['PHP_SELF'];?>">
<input type="textarea" name="query">
<input type="submit" value="Query!">
</form>

<?php
	if($_SERVER["REQUEST_METHOD"] == "POST"){
 	$query = $_POST['query'];
 	#CHANGE THIS SHIT!!!
 	$db = new mysqli('localhost', 'cs143', '', 'CS143');

 	if ($db->connect_errno > 0){
 		die('Unable to connect to database');
 	}

 	$result = $db->query($query);
 	$result_str = '';

 	echo "<table border=1>";
 	echo "<tr>" ;
 	$fields = $result -> fetch_fields();
 	foreach ($fields as $field){
 		echo  "<th>". $field->name . "</th>";
 	}
 	echo "</tr>";

 	while ($rowinfo = $result ->fetch_array(MYSQLI_NUM))
 	{	
 		echo "<tr>";
 		foreach ($rowinfo as $row){
 			echo  "<td>". $row. "</td>";
 		}
 		echo "</tr>";
 	}
 	echo "</table>";
 	echo $result_str;

 	
 }
?>


</body>

</html>