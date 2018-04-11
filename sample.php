<!DOCTYPE html>
<html>
<head>

</head>

<body>

<h1>PHP Calculator</h1>
Type an expression in the box </br>

<form method="post" action="<?php echo $_SERVER['PHP_SELF'];?>">
<input type="text" name="expression">
<input type="submit" value="Calculate">
</form>

<?php
 if($_SERVER["REQUEST_METHOD"] == "POST"){
 	$expression = $_POST['expression'];
 	if (empty($expression)){
 		echo "Empty expression";
 	} else {
 		$pattern2 = "/^([-+]? ?(\d+|\(\g<1>\))( ?[-+*\/] ?\g<1>)?)$/";
 		$pattern = "/^((?![0-9]).)+/";
 		if (preg_match($pattern2,$expression,$match)){
 			$result =eval("return ".$expression.";");
 			echo $result;

 		}
 		else{
 			echo "Bad expression";
 		}

 	}
 }
?>

</body>

</html>