from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask
from flask import request
from flask import send_file
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
	try:
		page_source = driver.page_source
		views_count = int(re.findall('(?<="video_view_count":)[0-9]*(?=,)', page_source)[0])
		return views_count
	except:
		return -1

def likes_count(shortcode):
	url = "https://www.instagram.com/p/" + shortcode
	driver.get(url)
	if (driver.title == "Page Not Found • Instagram"):
		return -2
	try:
		page_source = driver.page_source
		likes_count = int(re.findall('(?<="edge_media_preview_like":{"count":)[0-9]*(?=,)', page_source)[0])
		return likes_count
	except:
		return -1

def followers_count(username):
	url = "https://www.instagram.com/" + username + "?__a=1"
	driver.get(url)
	try:
		page_source = driver.page_source
		followers_count = int(re.findall('(?<="edge_followed_by":{"count":)[0-9]*(?=})', page_source)[0])
		return followers_count
	except:
		return -1

@app.route('/favicon.ico')
def favicon():
	return send_file('favicon.ico')

@app.route("/p/<shortcode>/", methods=['GET'])
def api_post(shortcode):
	likes_counter = str(likes_count(shortcode))
	views_counter = str(views_count(shortcode))
	data = {'shortcode':shortcode, 'likes_count':likes_counter, 'views_count':views_counter}
	response = app.response_class(response=json.dumps(data), mimetype='application/json')
	return response

@app.route("/<username>/", methods=['GET'])
def api_user(username):
	followers_counter = str(followers_count(username))
	data = {'username':username, 'followers_count':str(followers_counter)}
	response = app.response_class(response=json.dumps(data), mimetype='application/json')
	return response

@app.errorhandler(404)
def page_not_found(error):
	data = {'message':'not found'}
	response = app.response_class(response=json.dumps(data), status=404, mimetype='application/json')
	return response

app.run(host='0.0.0.0', port=18450)