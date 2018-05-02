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
    Date of Birth <input type = "text" name = "dob" placeholder = "Ex: 2001-10-22" />
    Date of Death <input type = "text" name = "dod" placeholder = "Ex: 2001-10-22" />
  </div>

  <button type = "submit" name = "submit" >Add</button>

</form>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['submit'])) {

      //TODO: add formatting checks
      $job = $_POST['job'];
      if(empty($job))exit("Select Actor or Director.");
      $firstname = $_POST['firstname'];
      $lastname = $_POST['lastname'];
      if(empty($firstname) or empty($lastname))exit("Need full name.");
      $gender = $_POST['gender'];
      if(empty($gender))exit("Enter gender.");
      $dob = $_POST['dob'];
      if(empty($dob))exit("Need birthdate.");
      $dod = $_POST['dod'];
      $date_birth = strtotime($dob);
      if($date_birth === FALSE)
      {
        exit("Date format.");
      }
      $date_birth=date("Y-m-d", $date_birth);
      $date_death=strtotime($dod);
        if($date_death === FALSE and !empty($dod))
        {
          exit("Date format.");
        }
      if(!empty($dod)){
        $date_death=date("Y-m-d", $date_death);
      }
      else
      {
        $date_death=null;
      }
      //check date syntax

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
        $query_actor->bind_param("isssss", $maxpersonid, $lastname, $firstname, $gender, $date_birth, $date_death);
        if ($query_actor->execute() === FALSE) {
          echo "Error: " . $query_actor . "<br>" . $db->error;
        }
      }
      else if ($job == "Director") {
        $stmt = $db->prepare("INSERT INTO Director (id, last, first, dob, dod) VALUES (?, ?, ?, ?, ?)");
        $stmt->bind_param("issss", $maxpersonid, $lastname, $firstname, $date_birth, $date_death);

        if ($stmt->execute() == FALSE) {
          echo "Error: " . $stmt . "<br>" . $db->error;
        }

      }
    }
  }

?>

</body>

</html>