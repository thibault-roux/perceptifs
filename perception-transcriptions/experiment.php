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
		<title>50 clics pour la Science</title>
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
				<p>Nous appelons référence une transcription exacte d'un audio vers du texte. Nous vous proposons deux hypothèses (appelées transcriptions) produites par des systèmes de reconnaissance de la parole. Choisissez la transcription qui vous parait la plus acceptable.&nbsp;</p>
				<p><b>Référence : </b><span id="fileName" style="border: 1px solid grey; border-radius: 0.75ex; padding-left: 0.6em; padding-right: 0.6em; box-shadow: 0px 0px 3px lightgrey; font-size: 110%; padding-top: 0.2em; line-height: 200%"></span></p>
				<h2><span id="fileName"></span></h2>
				<!-- <p><audio id="audioPlayer" controls preload src="">Audio non supporté. 😢</audio></p> -->
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
		 
		 function shuffle(array) {
			let currentIndex = array.length;
			let randomIndex;
			while (currentIndex > 0) {
				randomIndex = Math.floor(Math.random() * currentIndex);
				currentIndex --;
				[array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
			}
			return array;
		 }
		 
		 function setFile(index) {
			 let newFile = audioFiles[index];
			 // document.getElementById("audioPlayer").src = newFile.path;
			 document.getElementById("fileName").textContent = newFile.reference;
			 document.getElementById("progress").value = index+1;
			 let hypothesesList = "";
			 let i = 1;
			 for (hypName of shuffle(Object.keys(newFile.hypotheses))) {
				 let hypText = newFile.hypotheses[hypName];
				 let hypNode = '<div><h3>Transcription '+i+' :</h3><p>'+hypText+'</p><button onclick="answer(\''+hypName+'\')">Choisir la transcription '+i+'</button></div>';
				 hypothesesList += hypNode;
				 i += 1;
			 }
			 document.getElementById("hypotheses").innerHTML = hypothesesList;
		 }
		 
		 function answer(value) {
			 console.log("Debut de answer()")
			 // document.getElementById("audioPlayer").pause();
			 // answers.set(audioFiles[currentFileIndex].path, value);
			 answers.set(audioFiles[currentFileIndex].id, value);
			 currentFileIndex += 1;
			 if (currentFileIndex < audioFiles.length) {
				 setFile(currentFileIndex);
			 } else {
				 document.getElementById("hypotheses").innerHTML = "";
				 document.getElementById("currentTest").hidden = true;
				 let answerList =  "";
				 answers.forEach(function(answer, id) {
					 answerList += "<dt>"+id+"</dt><dd>"+answer+"</dd>";
				 });
				 document.getElementById("answerListRecap").innerHTML = answerList;
				 document.getElementById("answerList").value = JSON.stringify(Object.fromEntries(answers));
				 document.getElementById("finished").hidden = false;
			 }
			 console.log("Fin de answer()")
		 }
	 </script>
</html>
