<html>

<body>

<h2>Add a new actor or director!</h2>

<form method = "post">
  <div>
    <input type = "radio" name = "job" value = "Actor" /> Actor  
    <input type = "radio" name = "job" value = "Director" /> Director
  </div>

  <div>
    First Name <input type = "text" name = "firstname" placeholder = "First Name" />
    Last Name <input type = "text" name = "lastname" placeholder = "Last Name" />
  </div>

  <div>
    <input type = "radio" name = "gender" value = "Male" /> Male  
    <input type = "radio" name = "gender" value = "Female" /> Female
  </div>

  <div>
    Date of Birth <input type = "text" name = "dob" placeholder = "Date of Birth" />
    Date of Death <input type = "text" name = "dod" placeholder = "Date of Death" />
  </div>

  <button type = "submit" name = "submit" >Add</button>

</form>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {

      //TODO: add formatting checks
      $job = $_POST['job'];
      $firstname = $_POST['firstname'];
      $lastname = $_POST['lastname'];
      $gender = $_POST['gender'];
      $dob = $_POST['dob'];
      $dod = $_POST['dod'];

      //Connect to DB
      $db = new mysqli('localhost', 'cs143', '', 'TEST');

      if ($db->connect_errno > 0){
        die('Unable to connect to database');
      }

      //Get MaxPersonID
      $query_personid = 'SELECT * FROM MaxPersonID';
      $result = $db->query($query_personid);

      if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
          $maxpersonid = $row['id'];
        }
      }
      else {
        echo 'Error: No max person ID';
      }

      //Update MaxPersonID
      $updated_id = $maxpersonid + 1;
      $query_update = $db->prepare("UPDATE MaxPersonID SET id = ? WHERE id = ?");
      $query_update->bind_param("ii", $updated_id, $maxpersonid);
      if ($query_update->execute() === FALSE) {
        echo "Error: " . $query_update . "<br>" . $db->error;
      }

      //Insert in Actor table
      if ($job == "Actor") {
        $query_actor = $db->prepare("INSERT INTO Actor (id, last, first, sex, dob, dod) VALUES (?, ?, ?, ?, ?, ?)");
        $query_actor->bind_param("isssss", $maxpersonid, $lastname, $firstname, $gender, $dob, $dod);

        if ($query_actor->execute() === FALSE) {
          echo "Error: " . $query_actor . "<br>" . $db->error;
        }
      }
      else if ($job == "Director") {
        $query_director = $db->prepare("INSERT INTO Director (id, last, first, dob, dod) VALUES (?, ?, ?, ?, ?)");
        $query_director->bind_param("issss", $maxpersonid, $lastname, $firstname, $dob, $dod);

        if ($query_director->execute() === FALSE) {
          echo "Error: " . $query_director . "<br>" . $db->error;
        }
      }

    }
  }

?>

</body>

</html>