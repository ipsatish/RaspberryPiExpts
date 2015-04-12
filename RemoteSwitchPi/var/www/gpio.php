<!-- This page is requested by the JavaScript, it updates the pin's status and then print it -->
<?php
//Getting and using values
if (isset ($_GET["pin"]) && isset($_GET["status"]) ) {
	$pin = strip_tags($_GET["pin"]);
	$status = strip_tags($_GET["status"]);
	//Testing if values are numbers
	if ( (is_numeric($pin)) && (is_numeric($status)) && ($pin <= 7) && ($pin >= 0) && ($status == "0") || ($status == "1") ) {
		if ($status == "0" ) { 
			$status = "1";
		} else if ($status == "1" ) { 
			$status = "0";
		}
		$cmd = "sudo /var/www/gpio_control.py ".$pin." ".$status;
		exec ($cmd,$status,$return );
		echo ($status);
	}
	else { 
		echo ("fail");
	}
} 
//print fail if cannot use values
else { echo ("fail"); }
?>
