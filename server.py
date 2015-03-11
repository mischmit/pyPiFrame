import glob
import fnmatch
import os
import SimpleHTTPServer
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import datetime
import string
import json

allowedExtensions = ('.jpg', '.jpeg', '.JPEG', 'JPG')
start_time = datetime.datetime.now()
interval = 5

def get_current_image():
	curIndex = (datetime.datetime.now() - start_time).seconds / interval % len(files)
	return files[curIndex]

# Scans recursively for .jp?g files and collects
def get_files(path):
	matches = []
	for root, dirnames, filenames in os.walk(path):
		matches = matches + [os.path.join(root, filename) for filename in filenames if filename.endswith(allowedExtensions)]
	return [m.replace("\\", "/") for m in matches]

files = get_files('example_images')

class TimedHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/metadata.json":
			self.send_response(200)
			self.end_headers()
			current_image = get_current_image()
			self.wfile.write(json.dumps({"url": current_image, "duration": interval}))
		elif self.path == "/":
			self.send_response(200)
			self.end_headers()
			current_image = get_current_image()
			template = open("template.html").read()
			self.wfile.write(template)
		else:
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def serve_forever():
	PORT = 8001
	httpd = HTTPServer(("localhost", PORT), TimedHTTPRequestHandler)

	print "serving at port", PORT
	httpd.serve_forever()
	print start_time

def main():
	serve_forever()

if __name__ == '__main__':
	main()