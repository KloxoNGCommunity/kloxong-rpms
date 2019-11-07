<?php
ini_set('display_errors', 0);

include "compile.php";

rename("index.php", "index_adminer.php");
rename("adminer-{$VERSION}.php", "index.php");

Print("\n<p>Refresh this page!</p>");
?>