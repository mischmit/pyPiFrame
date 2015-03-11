import glob
import fnmatch
import os
import sys
import random
import SimpleHTTPServer
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import datetime
import json
import time

allowedExtensions = ('.jpg', '.jpeg', '.JPEG', 'JPG')
ignore_dir = "@eaDir"
start_time = datetime.datetime.now()
interval = 10

def get_metadata(file):
	return {"url": file, "time": time.ctime(os.path.getctime(file))}

def get_current_image():
	curIndex = (datetime.datetime.now() - start_time).seconds / interval % len(files)
	return files[curIndex]

# Scans recursively for .jp?g files and collects
def get_files(path):
	matches = []
	for root, dirnames, filenames in os.walk(path):
		try:
			dirnames.remove(ignore_dir)
		except ValueError:
			pass
		matches = matches + [os.path.join(root, filename) for filename in filenames if filename.endswith(allowedExtensions)]
	return [m.replace("\\", "/") for m in matches]

if len(sys.argv) == 2:
	path = sys.argv[1]
else:
	path = "example_images"

print os.path.join(os.getcwd(), path)
files = get_files(path)
print "Everyday im shuffelling ..."
random.shuffle(files)
print len(files), "Files"

class TimedHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/metadata.json":
			self.send_response(200)
			self.end_headers()
			current_image = get_current_image()

			metadata = get_metadata(current_image)
			metadata["duration"] = interval
			self.wfile.write(json.dumps(metadata))
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