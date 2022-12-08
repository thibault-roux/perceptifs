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
		<title>100 clics pour la science — Fin</title>
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
	echo '<p>Cette expérience est maintenant terminée. Merci de votre participation.</p>';
	
	$subjectID = str_replace('/','',$_SESSION['subjectID']);
	$experimentID = str_replace('/','',$_SESSION['experimentID']);
	
	// Record the results
	$file = fopen('results/'.$experimentID.'-'.$subjectID.'.json', 'w');
	$timestamp = date_format(date_create(), "Y-m-d H:i:s");
	fwrite($file, '{
		"name": "'.$_SESSION['subjectName'].'",
		"email": "'.$_SESSION['subjectEmail'].'",
		"age": "'.$_SESSION['subjectAge'].'",
		"language": "'.$_SESSION['subjectLanguage'].'",
		"nbOfLanguages": "'.$_SESSION['subjectNbOfLanguages'].'",
		"educationLevel": "'.$_SESSION['subjectEducationLevel'].'",
		"timestamp": "'.$timestamp.'",
		"ip": "'.$_SERVER['REMOTE_ADDR'].'",
		"answers": '.$_POST['answerList']
		.'}');
	fwrite($file, "\n");
	fclose($file);
	
	// Create the marker file indicating this run was completed.
	fclose(fopen("runs/".$experimentID."/completed"."/".$subjectID, "w"));
	
	// Delete the marker file indicating a run was under way.
	unlink("runs/".$experimentID."/started"."/".$subjectID);
	
	// Clean up.
	unset($_SESSION['experimentID']);
}
?>
		</section>
     </body>	 
</html>
