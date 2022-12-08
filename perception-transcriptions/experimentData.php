<?php

$experimentDataFilePath = "experimentData.json";
$experimentDataFile = fopen($experimentDataFilePath, "r") or die("Error: Unable to open experiment data file.");
$experimentJSONData = fread($experimentDataFile,filesize($experimentDataFilePath));
fclose($experimentDataFile);

$experiments = json_decode($experimentJSONData);

function selectExperiment($experiments, $subjectID) {
	// First, let's check whether the current user is already in the middle of a run.
	if (isset($_SESSION["experimentID"])) {
		foreach ($experiments as $experiment) {
			if ($experiment->id == $_SESSION["experimentID"]) {
				return $experiment;
			}
		}
	}
	
	umask(0007);
	// Let's find the first experiment of the list which has not been completed 3 times yet.
	foreach ($experiments as $experiment) {
		$maxRunsPerExperiment = 3; // Maximum allowed runs for each experiment.
		
		// A marker file is created in the folder ./runs/<expID>/completed/ after each complete run.
		$completedRunsDir = "runs/".$experiment->id."/completed";
		if (!is_dir($completedRunsDir)) {
			mkdir($completedRunsDir, 0770, true);
		}
		if (count(scandir($completedRunsDir)) >= ($maxRunsPerExperiment+2)) { // +2 for . and ..
			continue; // Experiment already done at least $maxRunsPerExperiment times => we skip to the next one.
		} else if (file_exists($completedRunsDir."/".$subjectID)) {
			continue; // Experiment already completed by the current user => we skip to the next one.
		}
		
		// Now, we check that there are not already $maxRunsPerExperiment users in the process of running this experiment.
		// A marker file is created in the folder ./runs/<expID>/started/ at the beginning of each run.
		$startedRunsDir = "runs/".$experiment->id."/started";
		if (!is_dir($startedRunsDir)) {
			mkdir($startedRunsDir, 0770, true);
		}
		$dirContent = scandir($startedRunsDir);
		if (count($dirContent) >= ($maxRunsPerExperiment+2)) { // +2 for . and ..
			// Let's remove marker files for runs that have not been completed within 2 hours.
			foreach ($dirContent as $relativeFilename) {
				$file = $startedRunsDir.'/'.$relativeFilename;
				if ((!is_dir($file)) && (time() - filemtime($file) > 3600*2)) {
					unlink($file);
				}
			}
			$dirContent = scandir($startedRunsDir);
		}
		if (count($dirContent) < ($maxRunsPerExperiment+2)) {
			// We've found our experiment. Let's create the marker file and return the info.
			fclose(fopen($startedRunsDir."/".$subjectID, "w"));
			$_SESSION["experimentID"] = $experiment->id;
			return $experiment;
		}
	}
	
	// If we get to here, all the experiments have been completed at least 3 times.
	// We pick one randomly among those not done by the current user.
	$experimentsNotRunByUser = array_filter($experiments, function($exp) { global $subjectID; return !file_exists("runs/".$exp->id."/completed"."/".$subjectID); });
	if (count($experimentsNotRunByUser) > 0) {
		$experiment = $experiments[array_rand($experiments)];
		fclose(fopen("runs/".$experiment->id."/started"."/".$subjectID, "w"));
		$_SESSION["experimentID"] = $experiment->id;
		return $experiment;
	}
	return null; // This user has already done everything.
}

$experiment = selectExperiment($experiments, $subjectID);

?>
