#!/usr/bin/env python
#lab 3
#taken from http://pointlessprogramming.wordpress.com/2011/02/13/python-cgi-tutorial-1/ 2016-01-20
#Copyright Nick Zarczynski

import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
 
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 8000)
handler.cgi_directories = ["/"]
 
httpd = server(server_address, handler)
httpd.serve_forever()
