<html>

<body>

<h2>Add a new review!!</h2>

<form method = "post">

  <div>
    Your Name <input type = "text" name = "name" placeholder = "Enter Your Name" />
  </div>

  <div>
    Movie <input type = "text" name = "movie" placeholder = "Movie Name" />
  </div>

  <div>
    Movie Rating
    <select name="rating">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
      <option value="5">5</option>
    </select>
  </div>

  <div>
    Comment <input type = "text" name = "comment"  />
  </div>

  <button type = "submit" name = "submit" >Add Review</button>

</form>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {

      //TODO: add formatting checks
      $name = $_POST['name'];
      $movie_name = $_POST['movie'];
      $rating = $_POST['rating'];
      $comment = $_POST['comment'];
      $time = date("Y-m-d H:m:s",time());

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
        echo "Error: Could not find movie";
      }

      if(!empty($movie)) 
      {
        $stmt = $db->prepare("INSERT INTO Review (name,time,mid,rating,comment) VALUES (?,?,?,?,?)");
        $stmt->bind_param("ssiis",$name,$time,$movie,$rating,$comment);
        if($stmt->execute() === FALSE)
        {
          echo "Error: " . $query_director . "<br>" . $db->error;
        }
      }
    }
  }

?>

</body>

</html>