<?php

session_start();


$files = glob("results/*.*");/* $files pour "lister" les fichiers - Mise en place de *.* pour dire que ce dossier contient une extension (par exemple .jpg, .php, etc... */
$compteur = count($files);/* Variable $compteur pour compter (count) les fichiers lister ($files) dans le dossier */
echo "<font color=#FF0000>$compteur</font>";
if ($compteur > 1) { echo " personnes ont participe a l'experience."; }
else { echo " personne ont participe a l'experience."; }



?>
