<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Raspberry Pi Home Automation</title>
	<meta http-equiv="refresh" content="10">
    </head>
 
    <body style="background-color: black;">
     <!-- On/Off button's picture -->
	 <?php
	 //this php script generate the first page in function of the gpio's status
	 $status = array (1, 1, 1, 1, 1, 1, 1, 1);
	 for ($i = 0; $i < count($status); $i++) {
		//set the pin's mode to output and read them
		$cmd = "sudo /var/www/gpio_control.py ".$i." -1";
		exec ($cmd,$status[$i], $return);
		//if off
		if ($status[$i][0] == 0 ) {
		echo ("<img id='button_".$i."' src='data/img/red/red_".$i.".jpg' alt='off'/>");
		}
		//if on
		if ($status[$i][0] == 1 ) {
		echo ("<img id='button_".$i."' src='data/img/green/green_".$i.".jpg' alt='on'/>");
		}	 
	 }
	 ?>
	 <!-- javascript -->
	 <script src="script.js"></script>
    </body>
</html>
