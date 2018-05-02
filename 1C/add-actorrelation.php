<html>

<body>

<h2>Add an actor to a movie!!</h2>

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
    Actor
    <select name="actor">
      <?php
         $db = new mysqli('localhost', 'cs143', '', 'TEST');

        if ($db->connect_errno > 0){
          die('Unable to connect to database');
        }

        $query_movieid = "SELECT CONCAT(first,\" \",last) as name,dob, id FROM Actor ORDER BY name ASC";
        $result = $db->query($query_movieid);
        while($row=$result->fetch_assoc())
        {
          echo "<option value=".$row['id'].">".$row['name']."(".$row['dob'].")"."</option>";
        }

      ?>
      </select>
  </div>

  <div>
    Role <input type = "text" name = "role"/>
  </div>

  <button type = "submit" name = "submit" >Add Actor</button>

</form>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {


      $get_string =  $_SERVER['QUERY_STRING'];
      if (empty ($get_string))
      {

        //TODO: add formatting checks
        $actor = $_POST['actor'];
        if(empty($actor))exit("Enter actor name.");
        $movie = $_POST['movie'];
        if(empty($movie))exit("Enter movie title.");
        $role = $_POST['role'];
        if(empty($role))exit("Enter actor role.");


        //query movie table for movie id
         //Connect to DB
        $db = new mysqli('localhost', 'cs143', '', 'TEST');

        if ($db->connect_errno > 0){
          die('Unable to connect to database');
        }

        
        //insert into movie actor
        $query_movieactor = $db->prepare("INSERT INTO MovieActor (mid, aid, role) VALUES (?, ?, ?)");
        $query_movieactor->bind_param("iis", $movie, $actor, $role);
          if ($query_movieactor->execute() === FALSE) {
            echo "Error: " . $query_actor . "<br>" . $db->error;
          }
      }

    }
  }

?>

</body>

</html>