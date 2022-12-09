<?php
session_start();

function guidv4() {
    // Generate 16 bytes (128 bits) of random data or use the data passed into the function.
    $data =  openssl_random_pseudo_bytes(16);
    assert(strlen($data) == 16);

    // Set version to 0100
    $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
    // Set bits 6-7 to 10
    $data[8] = chr(ord($data[8]) & 0x3f | 0x80);

    // Output the 36 character UUID.
    return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}


if (isset($_POST['name'])) {	
	// Assign an ID
	$_SESSION['subjectID'] = guidv4();
	$_SESSION['subjectName'] = $_POST['name'];
	$_SESSION['subjectAge'] = $_POST['age'];
	$_SESSION['subjectLanguage'] = $_POST['language'];
	$_SESSION['subjectNbOfLanguages'] = $_POST['nbLanguages'];
	$_SESSION['subjectEducationLevel'] = $_POST['educationLevel'];
	
	header('Location: experiment.php');
	exit();
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>50 clics pour la science</title>
		<link rel="stylesheet" type="text/css" href="https://demo-lia.univ-avignon.fr/demo-lia.css">
	</head>
    <body>
		<header class="bandeau_lia petit"></header>
		<section>
			<h1>50 clics pour la science</h1>
			<p>Cette série d’expériences ne doit être menée qu’une fois par sujet. Merci de vous identifier ci-dessous avant de commencer.</p>
			<p>
			<form method="post">
				<p>
					<label for="prenom">Nom complet :</label>
					<input type="text" name="name" id="name" required="Yes" size="60">
				</p>
				<p>
					<label for="age">Âge :</label>
					<input type="number" name="age" id="age" required="Yes" size="4" min="13" max="125">
				</p>
				<p>
					<label for="language">Langue maternelle :</label>
					<input type="text" name="language" id="language" required="Yes" size="60">
				</p>
				<p>
					<label for="nbLanguages">Nombre de langues parlées (français inclus) ? :</label>
					<input type="number" name="nbLanguages" id="nbLanguages" required="Yes" size="4" min="1" value="1">
				</p>
				<p>
					<label for="educationLevel">Votre plus haut niveau d’études :</label>
					<select name="educationLevel" id="educationLevel">
					  <option value="0">Baccalauréat</option>
					  <option value="2">Bac+2 (BTS, DUT, etc.)</option>
					  <option value="3">Bac+3 (licence)</option>
					  <option value="5">Bac+5 (master, ingénieur)</option>
					  <option value="8">Bac+8 ou plus (doctorat)</option>
					</select>
				</p>
				<input type="submit" value="Commencer l’expérience">
			</form>
		</section>
     </body>
</html>
