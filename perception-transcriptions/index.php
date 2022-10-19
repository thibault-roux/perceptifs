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


if (isset($_POST['name']) && isset($_POST['email'])) {	
	// Assign an ID
	$_SESSION['subjectID'] = guidv4();
	$_SESSION['subjectName'] = $_POST['name'];
	$_SESSION['subjectEmail'] = $_POST['email'];
	header('Location: experiment.php');
	exit();
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Les super expériences de Thibault</title>
		<link rel="stylesheet" type="text/css" href="https://demo-lia.univ-avignon.fr/demo-lia.css">
	</head>
    <body>
		<header class="bandeau_lia petit"></header>
		<section>
			<h1>Les super expériences de Thibault</h1>
			<p>Merci Teva. Je fais un test. Cette série d’expériences ne doit être menée qu’une fois par sujet. Merci de vous identifier ci-dessous avant de commencer.</p>
			<p>
			<form method="post">
				<p>
					<label for="prenom">Nom complet :</label>
					<input type="text" name="name" id="name" required="Yes" size="60">
				</p>
				<p>
					<label for="prenom">Adresse email :</label>
					<input type="text" name="email" id="email" required="Yes" size="60">
				</p>
				<input type="submit" value="Commencer l’expérience">
			</form>
		</section>
     </body>
</html>
