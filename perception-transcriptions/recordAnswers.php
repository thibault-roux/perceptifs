<?php
session_start();

if (!isset($_SESSION['subjectID'])) {
	header('Location: index.php');
	exit();
}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Les super expériences de Thibault — Fin</title>
		<link rel="stylesheet" type="text/css" href="https://demo-lia.univ-avignon.fr/demo-lia.css">
	</head>
    <body>
		<header class="bandeau_lia petit"></header>
		<section>
<?php
if (!isset($_POST['answerList'])) {
	echo '<h1>Erreur</h1>';
	echo '<p>Une erreur s’est produite. Veuillez recommencer l’expérience.</p>';
	echo '<p><button onclick="window.location=\'experiment.php\'">Recommencer</button></p>';
} else {
	echo '<h1>Merci</h1>';
	echo '<p>Cette expérience est maintenant terminée. Merci de votre participation. 😘</p>';
	
	// Record the results
	$basename = str_replace('/','',$_SESSION['subjectID']);
	$file = fopen('results/'.$basename.'.json', 'w');
	$timestamp = date_format(date_create(), "Y-m-d H:i:s");
	fwrite($file, '{
		"name": "'.$_SESSION['subjectName'].'", 
		"email": "'.$_SESSION['subjectEmail'].'",
		"age": "'.$_SESSION['subjectAge'].'", 
		"Langue": "'.$_SESSION['subjectLangue'].'",
		"NbrLang": "'.$_SESSION['subjectNbrLang'].'",
		"Etudes": "'.$_SESSION['subjectEtudes'].'",
		"timestamp": "'.$timestamp.'",
		"answers": '.$_POST['answerList'].'
	}');
	fwrite($file, "\n");
	fclose($file);
	
	session_unset();
	session_destroy();
}
?>
		</section>
     </body>	 
</html>
