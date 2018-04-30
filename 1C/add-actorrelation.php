<html>

<body>

<h2>Add an actor to a movie!!</h2>

<form method = "post">

  <div>
    Actor <input type = "text" name = "name" placeholder = "Full Name" />
  </div>

  <div>
    Movie <input type = "text" name = "movie" placeholder = "Movie Name" />
  </div>

  <div>
    Role <input type = "text" name = "role"/>
  </div>

  <button type = "submit" name = "submit" >Add Actor</button>

</form>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {

      //TODO: add formatting checks
      $name = $_POST['name'];
      $movie_name = $_POST['movie'];
      $role = $_POST['role'];
      $actor_names = explode(" ", $name);
      if (count($actor_names) < 2) {
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
        $actor = null;
        //query for actor id
        $query_actorid = "SELECT id FROM Actor WHERE first = \"".$actor_names[0]."\" AND last=\"".$actor_names[1]."\"";
        $result = $db->query($query_actorid);
        if ($result->num_rows > 0) {
          $row = $result->fetch_assoc();
            $actor = $row['id'];
          
        }
        else {
          exit("Could not find actor");
        }
      //insert into movie actor
      $query_movieactor = $db->prepare("INSERT INTO MovieActor (mid, aid, role) VALUES (?, ?, ?)");
      $query_movieactor->bind_param("iis", $movie, $actor, $role);
        if ($query_movieactor->execute() === FALSE) {
          echo "Error: " . $query_actor . "<br>" . $db->error;
        }

    }
  }

?>

</body>

</html>