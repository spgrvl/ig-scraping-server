from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask
from flask import request
import json
import re
import os

# Create an instance of Flask
app = Flask(__name__)

# Log to file and stdout
import logging
logging.basicConfig(filename='error.log',level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

if os.name == "nt":
	chrome_path = r"C:\chromedriver_win32\chromedriver.exe"
elif os.name == "posix":
	chrome_path = "/usr/lib/chromium-browser/chromedriver"
else:
	print("Error: Chrome path is not set for this os: " + os.name)

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

def views_count(shortcode):
	url = "https://www.instagram.com/p/" + shortcode
	driver.get(url)
	if (driver.title == "Page Not Found • Instagram"):
		return -2
	for _ in range (2):
		try:
			post_source = driver.page_source
			views_count = int(re.findall('(?<="video_view_count":)[0-9]*(?=,)',post_source)[0])
			break
		except:
			return -1
	return views_count

def likes_count(shortcode):
	url = "https://www.instagram.com/p/" + shortcode
	driver.get(url)
	if (driver.title == "Page Not Found • Instagram"):
		return -2
	for _ in range (2):
		try:
			post_source = driver.page_source
			likes_count = int(re.findall('(?<="edge_media_preview_like":{"count":)[0-9]*(?=,)',post_source)[0])
			break
		except:
			return -1
	return likes_count

@app.route("/views", methods=['GET'])
def api_views():
	if 'shortcode' in request.args:
		shortcode = str(request.args['shortcode'].strip("/"))
		views_counter = str(views_count(shortcode))
		data = {'shortcode':shortcode, 'views_count':str(views_counter)}
		response = app.response_class(response=json.dumps(data), mimetype='application/json')
		return response
	else:
		data = {'message':'no shortcode provided'}
		response = app.response_class(response=json.dumps(data), status=400, mimetype='application/json')
		return response

@app.route("/likes", methods=['GET'])
def api_likes():
	if 'shortcode' in request.args:
		shortcode = str(request.args['shortcode'].strip("/"))
		likes_counter = str(likes_count(shortcode))
		data = {'shortcode':shortcode, 'likes_count':str(likes_counter)}
		response = app.response_class(response=json.dumps(data), mimetype='application/json')
		return response
	else:
		data = {'message':'no shortcode provided'}
		response = app.response_class(response=json.dumps(data), status=400, mimetype='application/json')
		return response

@app.errorhandler(404)
def page_not_found(error):
	data = {'message':'not found'}
	response = app.response_class(response=json.dumps(data), status=404, mimetype='application/json')
	return response

app.run(host='0.0.0.0', port=18450)