<?php
$started = time();
while (time() - $started < 3) {
  /* busy waiting for 3 seconds before returning to simulate some CPU intensive computations */ 
}
?>
<html>
 <head>
  <title>Hello World!</title>
 </head>
 <body>
 <p>
 Hello from <?php echo gethostname(); ?> 
 </p>
 </body>
</html>
