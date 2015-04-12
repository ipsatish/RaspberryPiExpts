<?php
    $dirname = "img";
    $dir = opendir($dirname);
    echo '<form action="delete.php" method="get">';
    echo '<select name="file2">';
    while(false != ($file = readdir($dir)))
    {
        if(($file != ".") and ($file != ".."))
        {
            echo "<option value=".$file.">$file</option>";
        }
    }
    echo '</select>';
    echo '<input type="submit" value="Delete" class="submit" />';
    echo '</form>';
?>
