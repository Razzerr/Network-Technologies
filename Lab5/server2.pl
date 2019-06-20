  use HTTP::Daemon;
  use HTTP::Status;  
  use IO::File;
  $WEBDIR = 'C:\Users\University\Desktop\4th semester\WWW\Projekt 1';
  my $d = HTTP::Daemon->new(
           LocalAddr => 'DESKTOP-PUEBIU8',
           LocalPort => 4321,
       )|| die;   
  print "Please contact me at: <URL:", $d->url, ">\n";
  while (my $c = $d->accept) {
      while (my $r = $c->get_request) {
		  if ($r->method eq 'GET') {
		  $file_s = $r->url;
			if($file_s eq "/"){
              $file_s= "./main.html";
			}
			$c->send_file_response($WEBDIR.$file_s);
          }
          else {
              $c->send_error(RC_FORBIDDEN)
          }
      }
      $c->close;
      undef($c);
  }
