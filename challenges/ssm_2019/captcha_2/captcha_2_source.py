<?php 

if(isset($_GET['source'])){
	echo "<pre>";
	echo htmlentities(file_get_contents(__FILE__));
	echo "</pre>";
	die();
}

session_start();
if(!isset($_SESSION['wins'])){
	$_SESSION['wins'] = 0;
}
if(!isset($_SESSION['errors'])){
	$_SESSION['errors'] = 0;
}

$roundStart = 1000000;
if(!isset($_COOKIE['round']) || !is_numeric($_COOKIE['round']) || (int)$_COOKIE['round'] >= PHP_INT_MAX){
	setcookie("round", $roundStart);
	$_COOKIE['round'] = $roundStart;
}
$round = (int)$_COOKIE['round'];

//Make it more difficult with every round
$rnd =  mt_rand(1, $round);
//Add some randomness
srand(time());
$rnd &= rand();
$sizelimit = $roundStart;
$rnd = $rnd % $sizelimit;
$captchaNum = $rnd;

for ($i=0; $i < 7; $i++) {
	$choice = rand(1,4);
	if ($choice == 1) {
		$rnd &= rand(1,$sizelimit);
	} else if($choice == 2) {
		$rnd |= rand(1,$sizelimit);
	} else if($choice == 3) {
		$rnd ^= rand(1,$sizelimit);
	} else if($choice == 4) {
		$rnd += rand(1,$sizelimit);
	}
}
$rnd = $rnd % $sizelimit;

if(isset($_POST['num']) && is_numeric($_POST['num'])){

	if(md5($_POST['num']) === md5($captchaNum)){
		setcookie("round", $round + 1);
		$_COOKIE['round'] = $round + 1;
		$_SESSION['wins']++;
		echo "Correct guess!";
	} else {
		$_SESSION['errors']++;
		if($_SESSION['errors'] > 5){
			setcookie("round", $roundStart);
			$_COOKIE['round'] = $roundStart;
			$_SESSION['wins'] = 0;
			$_SESSION['errors'] = 0;
		}
		echo "Wrong guess!";
	}

	if($round < $roundStart){
		echo "No cheating!";
		$_SESSION['wins'] = 0;
	}

	if($_SESSION['wins'] > 50){
		echo "CONGRATS! ".file_get_contents("../flag.txt");
	}
	die();
}
 ?>

<!DOCTYPE html>
<html>
<head>
	<title>Captcha</title>
</head>
<body>
	<h1>Captcha</h1>
	<p>Lös captchan 100 gånger utan att misslyckas för att visa att du är en robot.</p>
	<p>Antal lösningar: <?php echo $_SESSION['wins']; ?></p>
	<p>Captcha: <?php echo $rnd; ?></p>
	<p>Source: <a href="/index.php?source=ja_tack">länk</a></p>
	<p>Make a guess:</p>
	<form method="post" action="/index.php">
		<input type="text" name="num">
		<input type="submit" name="s">
	</form>
</body>
</html>
