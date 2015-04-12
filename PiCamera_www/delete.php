<?php
    $dirpath = "img";
    $file_to_delete = $_GET['file2'];
    echo "DEBUG: file to be deleted: $file2"	
    if ( unlink ($dirpath.'/'.$file_to_delete) ) {
        echo $file_to_delete . " deleted.";
    } else {
        echo "Error.";
    }
    header('location:backto prev');
?
