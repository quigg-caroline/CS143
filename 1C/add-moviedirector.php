<html>

<body>

<h2>Add an director to a movie!!</h2>

<form method = "post">

 <div>
    Movie
    <select name="movie">
      <?php
         $db = new mysqli('localhost', 'cs143', '', 'TEST');

        if ($db->connect_errno > 0){
          die('Unable to connect to database');
        }

        $query_movieid = "SELECT title, year,id FROM Movie ORDER BY title ASC";
        $result = $db->query($query_movieid);
        while($row=$result->fetch_assoc())
        {
          echo "<option value=".$row['id'].">".$row['title']."(".$row['year'].")"."</option>";
        }

      ?>
      </select>
  </div>

  <div>
    Director
    <select name="director">
      <?php
         $db = new mysqli('localhost', 'cs143', '', 'TEST');

        if ($db->connect_errno > 0){
          die('Unable to connect to database');
        }

        $query_movieid = "SELECT CONCAT(first,\" \",last) as name,dob, id FROM Director ORDER BY name ASC";
        $result = $db->query($query_movieid);
        while($row=$result->fetch_assoc())
        {
          echo "<option value=".$row['id'].">".$row['name']."(".$row['dob'].")"."</option>";
        }

      ?>
      </select>
  </div>

  <button type = "submit" name = "submit" >Add Director</button>

</form>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {

      //TODO: add formatting checks
      $movie= $_POST['movie'];
              if(empty($movie))exit("Enter movie name.");
      $did = $_POST['director'];
              if(empty($did))exit("Enter director name.");
    

      //query movie table for movie id
       //Connect to DB
      $db = new mysqli('localhost', 'cs143', '', 'TEST');

      if ($db->connect_errno > 0){
        die('Unable to connect to database');
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