<?php

/*
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
*/

echo "<meta content=\"True\" name=\"HandheldFriendly\" />";
echo "<meta content=\"width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;\" name=\"viewport\" />";
echo "<meta name=\"viewport\" content=\"width=device-width\" />";

$PFAD=dirname(__FILE__);


if(isset($_FILES["uploadFiles"]))
{
	if(!is_dir($PFAD."/preview/")) { mkdir($PFAD."/preview/");}
	if(!is_dir($PFAD."/files/")) { mkdir($PFAD."/files/");}
	
	foreach ($_FILES["uploadFiles"]["error"] as $key => $error) {
		//var_dump($_FILES["uploadFiles"]);
		$fileName = $_FILES["uploadFiles"]["name"][$key];
		// sanitize user-supplied filename to prevent injections
		// https://stackoverflow.com/a/2021729
		// Remove anything which isn't a word, whitespace, number
		// or any of the following caracters -_~,;[]().
		// If you don't need to handle multi-byte characters
		$fileName = preg_replace("([^\w\s\d\-_~,;\[\]\(\).])", '', $fileName);
		if ($error == UPLOAD_ERR_OK) {
			$fileTmpLoc = $_FILES["uploadFiles"]["tmp_name"][$key];
			$imageMime = mime_content_type($_FILES['uploadFiles']['tmp_name'][$key]);
			switch ($imageMime)
			{
				case "image/jpeg": $fileExt = "jpg"; break;
				case "image/png": $fileExt = "png"; break;
				case "image/gif": $fileExt = "gif"; break;
				case "video/mp4": $fileExt = "mp4"; break;
				default: 
				$fileExt = strtolower(end(explode('.', $fileName)));
				if ($fileName == $fileExt) { $fileExt = "";}
				break;
		
			}

			if ($fileExt == "") {
				$fileNewName=strtok($fileName, ".");
			} else {
				$fileNewName=strtok($fileName, ".")."."."$fileExt";
			}
			$fileNewLoc=$PFAD."/files/".$fileNewName;
			if (file_exists($fileNewLoc)) {
				echo "$fileTmpLoc".hash_file('sha256', $fileTmpLoc);
				echo "<br/>";
			        echo "$fileNewLoc".hash_file('sha256', $fileNewLoc); 
				if (hash_file('sha256', $fileTmpLoc) == hash_file('sha256', $fileNewLoc)) {
					echo "<div style='color:gray;'>file $fileName already there, ignoring</div></br>";
					continue ;
				}	
				else {
					$r = substr(str_shuffle(str_repeat($x='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', ceil(10/strlen($x)) )),1,10);
					if ($fileExt == "") {
						$fileNewName=strtok($fileName, ".")."_".$r;
					} else {
						$fileNewName=strtok($fileName, ".")."_".$r."."."$fileExt";
					}
					$fileNewLoc=$PFAD."/files/".$fileNewName;
				}
			}
			move_uploaded_file($fileTmpLoc, $fileNewLoc);
			echo "<div style='color:green;'>file $fileName successfully uploaded</div></br>";
			if ($imageMime == "image/jpeg" || $imageMime == "image/png")
			{
				#Generate small thumbnail
				$theImage = new Imagick($fileNewLoc);
				$theImage->stripImage();
				$theImage->writeImage($fileNewLoc);
				$theImage->thumbnailImage(240,0,FALSE);
				$theImage->borderImage("black",2,2);
				$theImage->writeImage($PFAD."/preview/".$fileNewName);
				$theImage->destroy();
			}
		}
		else { echo "<div style='color:red;'>upload of $fileName failed</div><br/>"; }
	}
}


echo "Bitte Bilder auswaehlen, dann auf hochladen klicken.<br/>";
echo "<br/>";
echo "Bilder koennen unten eingesehen werden, aber nur Klaus kann am Ende alle runterladen.<br/>";
echo "<br/>";
echo "Upload kann dauern - PRO BILD mehrere Sekunden und PRO VIDEO sogar Minuten - bitte geduldig sein nach dem Druecken und nicht alle 1000 Bilder auf einmal.<br/>";
echo "<br/>";
echo "Wenn es nicht klappt mit weniger auf einmal versuchen!<br/>";
echo "<br/>";
echo "<br/>";
        echo "<form method=\"post\" action=\"\" enctype=\"multipart/form-data\">\n";
        echo "<input name=\"uploadFiles[]\" id=\"filesToUpload\" type=\"file\" accept=\"image/*,video/*\" multiple=\"\"/>\n";
        echo "<input type=\"submit\" value=\"Hier nach dem Auswaehlen zum Upload druecken.\">\n";
	echo "</form>";
echo "<br/>";

	$nr=count(glob($PFAD."/files/*"));
	$jpg=count(glob($PFAD."/files/*.jpg"));
	$mov=count(glob($PFAD."/files/*.mp4"))+count(glob($PFAD."/files/*.mov"));;
	echo "Aktuell sind auf dem Server $nr Dateien, davon mindestens $jpg Bilder und $mov Videos<br/>";
	echo "Vorschau der Bilder:</br>";
echo "<br/>";
echo "<br/>";

	echo "<ul>";
	foreach (glob($PFAD."/files/*") as $i) {
		$f = basename($i);
		if (file_exists($PFAD."/preview/".$f)) {
			echo "<li>$f</br><img src=\"./preview/$f\" alt=\"$f\" /></li>";
		}
		else {
			echo "<li>".$f."</li>";
		}
	}
	echo "</ul>";
        
?>

