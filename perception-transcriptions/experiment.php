<?php
	session_start();

	if (!isset($_SESSION["subjectID"])) {
		header('Location: index.php');
		exit();
	}

	include 'experimentData.php';
?>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Les super expériences de Thibault — <?php echo $experimentTitle; ?></title>
		<link rel="stylesheet" type="text/css" href="https://demo-lia.univ-avignon.fr/demo-lia.css">
	</head>
    <body>
		<header class="bandeau_lia petit"></header>
		<section>
			<h1>Expérience 1
				<progress id="progress" value="0" max="100" style="margin-left: 3em;"></progress>
			</h1>
			<div id="currentTest">
				<h2><span id="fileName"></span></h2>
				<p><audio id="audioPlayer" controls preload src="">Audio non supporté. 😢</audio></p>
				<div id="hypotheses">
					<p><button name="answerButton" onclick="answer('A')">⇢ Réponse A</button> <button name="answerButton" onclick="answer('B')">⇢ Réponse B</button></p>
				</div>
			</div>
		</section>
		<section id="recap" hidden>
			<h2>Vos réponses :</h2>
			<p>
				<dl id="answerListRecap">
				</dl>
			</p>
			<form method="post" action="recordAnswers.php">
				<input type="hidden" name="answerList" id="answerList" value="">
				<input type="submit" value="Envoyer les réponses">
			</form>
		</section>
     </body>
	 
	 <script type="text/javascript">
		 const audioFiles = [
<?php
	shuffle($audioList);
	foreach ($audioList as $audioFile) {
		echo $audioFile.',';
	}
?>
		 ];
		 var currentFileIndex = 0;
		 var answers = new Map();
		 document.getElementById("progress").max = audioFiles.length;
		 setFile(0);
		 
		 
		 function setFile(index) {
			 let newFile = audioFiles[index];
			 document.getElementById("audioPlayer").src = newFile.path;
			 document.getElementById("fileName").textContent = newFile.name;
			 document.getElementById("progress").value = index+1;
			 let hypothesesList = "";
			 for ([hypName, hypText] of newFile.hypotheses.entries()) {
				 let hypNode = '<div><h3>Réponse '+hypName+' :</h3><p>'+hypText+'</p><button onclick="answer(\''+hypName+'\')">Choisir la réponse '+hypName+'</button></div>';
				 hypothesesList += hypNode;
			 }
			 document.getElementById("hypotheses").innerHTML = hypothesesList;
		 }
		 
		 function answer(value) {
			 document.getElementById("audioPlayer").pause();
			 answers.set(audioFiles[currentFileIndex].name, value);
			 currentFileIndex += 1;
			 if (currentFileIndex < audioFiles.length) {
				 setFile(currentFileIndex);
			 } else {
				 document.getElementById("hypotheses").innerHTML = "";
				 document.getElementById("currentTest").hidden = true;
				 let answerList =  "";
				 answers.forEach(function(answer, fileName) {
					 answerList += "<dt>"+fileName+"</dt><dd>"+answer+"</dd>";
				 });
				 document.getElementById("answerListRecap").innerHTML = answerList;
				 document.getElementById("answerList").value = JSON.stringify(Object.fromEntries(answers));
				 document.getElementById("recap").hidden = false;
			 }
		 }
	 </script>
</html>
