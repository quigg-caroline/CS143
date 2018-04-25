<html>

<body>

<h2>Add a new movie!</h2>

<form method = "post">

  <div>
    Title <input type = "text" name = "title" placeholder = "Title" />
    Company <input type = "text" name = "company" placeholder = "Company" />
    Year <input type = "text" name = "year" placeholder = "Year" />
    MPAA Rating 
    <select name = "rating">
      <option value = "G">G</option>
      <option value = "NC-17">NC-17</option>
      <option value = "PG">PG</option>
      <option value = "PG-13">PG-13</option>
      <option value = "R">R</option>
    </select>
  </div>

  <div>
    Genre:
    <input type = "checkbox" name = "genre[]" value = "Action" /> Action  
    <input type = "checkbox" name = "genre[]" value = "Adult" /> Adult
    <input type = "checkbox" name = "genre[]" value = "Adventure" /> Adventure  
    <input type = "checkbox" name = "genre[]" value = "Animation" /> Animation
    <input type = "checkbox" name = "genre[]" value = "Comedy" /> Comedy  
    <input type = "checkbox" name = "genre[]" value = "Crime" /> Crime
    <input type = "checkbox" name = "genre[]" value = "Documentary" /> Documentary 
    <input type = "checkbox" name = "genre[]" value = "Drama" /> Drama
    <input type = "checkbox" name = "genre[]" value = "Family" /> Family  
    <input type = "checkbox" name = "genre[]" value = "Fantasy" /> Fantasy
  </div>

  <button type = "submit" name = "submit" >Add</button>

</form>

<?php
	if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $title = $_POST['title'];
    $company = $_POST['company'];
    $year = $_POST['year'];
    $rating = $_POST['rating'];
    if (!empty($_POST['genre'])) {
      foreach($_POST['genre'] as $selected)
        echo $selected. '</br>';
    }

    $db = new mysqli('localhost', 'cs143', '', 'TEST');

    if ($db->connect_errno > 0){
      die('Unable to connect to database');
    }
  }
?>

</body>

</html>