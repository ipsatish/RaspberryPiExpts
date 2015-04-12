<html>
<head>
<meta http-equiv="Content-Type" content="text/html">
<title>Admin Page - Access to delete images in folder</title>
<style type="text/css">
button {
	color: #F00;
	font-weight:bold;
	border:1px solid #F00;
	background-color:#900
	margin-left:5px;
	
}
body {
    margin: 0 5px 10px;
    padding: 0;
    background: #acacac;
    text-align: left;
}
td {
    padding: 0 0 50px;
    text-align: left;
    font: 9px sans-serif;
}
table {
    width: 100%;
}
img {
    display: block;
    margin: 5px 5px 5px;
    max-width: 150px;
    outline: none;
}
img:active {
    max-width: 100%;
}
a:focus {
    outline: none;
}
</style>
</head>
<body>
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
echo "<button type='submit' value='Delete'> Delete</button>";
}
closedir($dir_handle);
?>
</form>
</body>
</html>
