<html>
<head>
<meta http-equiv="Content-Type" content="text/html">
<title>Show images in folder</title>
<style type="text/css">
body {
    margin: 0 auto 20px;
    padding: 0;
    background: #acacac;
    text-align: center;
}
td {
    padding: 0 0 50px;
    text-align: center;
    font: 9px sans-serif;
}
table {
    width: 100%;
}
img {
    display: block;
    margin: 20px auto 10px;
    max-width: 900px;
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
$folder = 'img/';
$filetype = '*.*';
$files = glob($folder.$filetype);
$count = count($files);
echo '<table>';
for ($i = 0; $i < $count; $i++) {
    echo '<tr><td>';
    echo '<a name="'.$i.'" href="#'.$i.'"><img src="'.$files[$i].'" /></a>';
    echo substr($files[$i],strlen($folder),strpos($files[$i], '.')-strlen($folder));
    echo '</td></tr>';
}
echo '</table>';
?>
</body>
</html>

Change the code to sort the files by date/time

<?php
$folder = 'img/';
$filetype = '*.*';
$files = glob($folder.$filetype);
$count = count($files);
 
$sortedArray = array();
for ($i = 0; $i < $count; $i++) {
    $sortedArray[date ('YmdHis', filemtime($files[$i]))] = $files[$i];
}
 
ksort($sortedArray);
echo '<table>';
foreach ($sortedArray as &$filename) {
    #echo '<br>' . $filename;
    echo '<tr><td>';
    echo '<a name="'.$filename.'" href="#'.$filename.'"><img src="'.$filename.'" /></a>';
    echo substr($filename,strlen($folder),strpos($filename, '.')-strlen($folder));
    echo '</td></tr>';
}
echo '</table>';
?>

Change ksort to krsort

