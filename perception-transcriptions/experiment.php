<?php
	session_start();

	if (!isset($_SESSION["subjectID"])) {
		header('Location: index.php');
		exit();
	}
	$subjectID = str_replace('/','',$_SESSION['subjectID']); // Just in case.
		
	include 'experimentData.php';
		
	if ($experiment == null) { // Unable to find an experiment to run.
		header('Location: index.php');
		exit();
	}
?>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>100 clics pour la science</title>
		<link rel="stylesheet" type="text/css" href="https://demo-lia.univ-avignon.fr/demo-lia.css">
	</head>
    <body>
		<header class="bandeau_lia petit"></header>
		<section>
			<h2>
				Progression :
				<progress id="progress" value="0" max="100" style="margin-left: 1em;"></progress>
			</h2>
			<div id="currentTest">
				<!-- <h2><span id="fileName"></span></h2> -->
				<p><audio id="audioPlayer" controls preload src="">Audio non supporté. 😢</audio></p>
				<div id="hypotheses">
				</div>
			</div>
		</section>
		<section id="finished" hidden>
			<div id="recap" hidden>
				<h2>Vos réponses :</h2>
				<p>
					<dl id="answerListRecap">
					</dl>
				</p>
			</div>
			<p>Vous avez répondu à toutes les questions. Merci de cliquer sur le bouton ci-dessous pour enregistrer vos réponses.</p>
			<form method="post" action="recordAnswers.php">
				<input type="hidden" name="answerList" id="answerList" value="">
				<input type="submit" value="Envoyer les réponses">
			</form>
		</section>
     </body>
	 
	 <script type="text/javascript">
		 const audioFiles = 
<?php
	shuffle($experiment->audioList);
	echo json_encode($experiment->audioList).';';
?>
		 
		 var currentFileIndex = 0;
		 var answers = new Map();
		 document.getElementById("progress").max = audioFiles.length;
		 setFile(0);
		 
		 
		 function setFile(index) {
			 let newFile = audioFiles[index];
			 document.getElementById("audioPlayer").src = newFile.path;
			 // document.getElementById("fileName").textContent = newFile.name;
			 document.getElementById("progress").value = index+1;
			 let hypothesesList = "";
			 for (hypName in newFile.hypotheses) {
				 let hypText = newFile.hypotheses[hypName];
				 let hypNode = '<div><h3>Réponse '+hypName+' :</h3><p>'+hypText+'</p><button onclick="answer(\''+hypName+'\')">Choisir la réponse '+hypName+'</button></div>';
				 hypothesesList += hypNode;
			 }
			 document.getElementById("hypotheses").innerHTML = hypothesesList;
		 }
		 
		 function answer(value) {
			 document.getElementById("audioPlayer").pause();
			 answers.set(audioFiles[currentFileIndex].path, value);
			 currentFileIndex += 1;
			 if (currentFileIndex < audioFiles.length) {
				 setFile(currentFileIndex);
			 } else {
				 document.getElementById("hypotheses").innerHTML = "";
				 document.getElementById("currentTest").hidden = true;
				 let answerList =  "";
				 answers.forEach(function(answer, path) {
					 answerList += "<dt>"+path+"</dt><dd>"+answer+"</dd>";
				 });
				 document.getElementById("answerListRecap").innerHTML = answerList;
				 document.getElementById("answerList").value = JSON.stringify(Object.fromEntries(answers));
				 document.getElementById("finished").hidden = false;
			 }
		 }
	 </script>
</html>
