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
    <input type = "checkbox" name = "genre[]" value = "Horror" /> Horror
    <input type = "checkbox" name = "genre[]" value = "Musical" /> Musical
    <input type = "checkbox" name = "genre[]" value = "Romance" /> Romance
    <input type = "checkbox" name = "genre[]" value = "Sci-Fi" /> Sci-Fi
    <input type = "checkbox" name = "genre[]" value = "Short" /> Short
    <input type = "checkbox" name = "genre[]" value = "Thriller" /> Thriller
    <input type = "checkbox" name = "genre[]" value = "War" /> War
    <input type = "checkbox" name = "genre[]" value = "Western" /> Western

  </div>

  <button type = "submit" name = "submit" >Add</button>

</form>

<?php
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {

      //TODO: add formatting checks
      $title = $_POST['title'];
      if(empty($title))exit("Enter movie title.");
      $company = $_POST['company'];
      if(empty($company))exit("Enter production company.");
      $year = $_POST['year'];
      if(empty($year))exit("Enter year.");
      $rating = $_POST['rating'];
      if(empty($rating))exit("Enter MPAA rating.");
      if (empty($_POST['genre']))exit("Enter a genre.");

      if(strlen($year)<4)
      {
        exit("Year format");
      }
      $year = strtotime($year);
      if($year === FALSE)
      {
        exit("Year format");
      }
      $year=date("Y", $year);
      //Connect to DB
      $db = new mysqli('localhost', 'cs143', '', 'TEST');

      if ($db->connect_errno > 0){
        die('Unable to connect to database');
      }

      //Get MaxMovieID
      $query_movieid = 'SELECT * FROM MaxMovieID';
      $result = $db->query($query_movieid);

      if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
          $maxmovieid = $row['id'];
        }
      }
      else {
        echo 'Error: No max movie ID';
      }

      //Update MaxMovieID
      $updated_id = $maxmovieid + 1;
      $query_update = $db->prepare("UPDATE MaxMovieID SET id = ? WHERE id = ?");
      $query_update->bind_param("ii", $updated_id, $maxmovieid);
      if ($query_update->execute() === FALSE) {
        echo "Error: " . $query_update . "<br>" . $db->error;
      }

      //Insert into Movie table
      $query_movie = $db->prepare("INSERT INTO Movie (id, title, year, rating, company) VALUES (?, ?, ?, ?, ?)");
      $query_movie->bind_param("isiss", $maxmovieid, $title, $year, $rating, $company);

      if ($query_movie->execute() === FALSE) {
        echo "Error: " . $query_movie . "<br>" . $db->error;
      }
      //Insert into MovieGenre table
      if (!empty($_POST['genre'])) {
        foreach($_POST['genre'] as $selected){
        $query_genre = $db->prepare("INSERT INTO MovieGenre (mid, genre) VALUES (?, ?)");
        $query_genre->bind_param("is", $maxmovieid, $selected);
        if ($query_genre->execute() === FALSE) {
          echo "Error: " . $query_genre . "<br>" . $db->error;
        }
      }
     }
   }
  }
?>

</body>

</html>