<html>
<body>
	<h2>Movie Information Page</h2>
	<?php
		$get_string =  $_SERVER['QUERY_STRING'];
		parse_str($get_string, $get_array);
		echo $get_array['id'];
		echo "<h3>Movie Info</h3>";


	?>
</body>
</html>