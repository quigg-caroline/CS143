<html>

<body>

<h2>Add an director to a movie!!</h2>

<form method = "post">

  <div>
    Movie <input type = "text" name = "movie" placeholder = "Movie Name" />
  </div>

  <div>
    Director <input type = "text" name = "name" placeholder = "Full Name" />
  </div>

  <button type = "submit" name = "submit" >Add Director</button>

</form>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {

      //TODO: add formatting checks
      $movie_name = $_POST['movie'];
      $director = $_POST['name'];
      $director_names = explode(" ", $director);
      if (count($director_names) < 2) {
        exit("Enter first and last name for actor");
      }

      //query movie table for movie id
       //Connect to DB
      $db = new mysqli('localhost', 'cs143', '', 'TEST');

      if ($db->connect_errno > 0){
        die('Unable to connect to database');
      }

      $query_movieid = "SELECT id FROM Movie WHERE title = \"".$movie_name."\"";
      $result = $db->query($query_movieid);
      $movie = null;
      if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $movie = $row['id'];
      }
      else {
        exit("Error: Could not find movie");
      }
        $did = null;
        //query for actor id
        $query_directorid = "SELECT id FROM Director WHERE first = \"".$director_names[0]."\" AND last=\"".$director_names[1]."\"";
        $result = $db->query($query_directorid);
        if ($result->num_rows > 0) {
          $row = $result->fetch_assoc();
            $did = $row['id'];
          
        }
        else {
          exit("Could not find director");
        }
      //insert into movie actor
      $query_moviedirector = $db->prepare("INSERT INTO MovieDirector (mid, did) VALUES (?, ?)");
      $query_moviedirector->bind_param("ii", $movie, $did);
        if ($query_moviedirector->execute() === FALSE) {
          echo "Error: " . $query_actor . "<br>" . $db->error;
        }

    }
  }

?>

</body>

</html>