<?php
$path = "img";
if(isset($_POST['file']) && is_array($_POST['file']))
{
	foreach($_POST['file'] as $file)
	{	
		unlink($path . "/" . $file) or die("Failed to delete file");
	}
}
?>
<form name="form1" method="post">
<?php
$path = "img";
$dir_handle = @opendir($path) or die("Unable to open folder");
while (false !== ($file = readdir($dir_handle))) {
if($file == "index.php")
continue;
if($file == ".")
continue;
if($file == "..")
continue;
$file1 = $path;
$file1.="/";
$file1.=$file;
echo "<img src='$file1' alt='$file'><br />";
echo "<input type='CHECKBOX' name='file[]' value='$file'>";
}
closedir($dir_handle);
?>
<input type="submit" name="Delete" value="Delete">
</form>
