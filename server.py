from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask
from flask import request
from flask import send_file
import json
import re
import os
from sys import argv

# Create an instance of Flask
app = Flask(__name__)

# Log to file and stdout
import logging
logging.basicConfig(filename='error.log',level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

# Set chromedriver path based on os
if os.name == "nt":
    chrome_path = r"C:\chromedriver_win32\chromedriver.exe"
elif os.name == "posix":
    chrome_path = "/usr/lib/chromium-browser/chromedriver"
else:
    print("Error: Chrome path is not set for this os: " + os.name)

# Open headless chromedriver and change user-agent
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
driver = webdriver.Chrome(chrome_path, options=chrome_options)

# Instagram Login (optional)
if "--login" in argv:
    import ig_login
    ig_login.login(driver)

def get_post_data(shortcode):
    url = "https://www.instagram.com/p/" + shortcode
    driver.get(url)
    if (driver.title == "Page Not Found • Instagram"):
        return -2
    page_source = driver.page_source
    try:
        likes_count = re.findall('(?<="edge_media_preview_like":{"count":)[0-9]*(?=,)', page_source)[0]
    except:
        likes_count = -1
    try:
        views_count = re.findall('(?<="video_view_count":)[0-9]*(?=,)', page_source)[0]
    except:
        views_count = -1
    return likes_count, views_count

def get_user_data(username):
    url = "https://www.instagram.com/" + username + "?__a=1"
    driver.get(url)
    if driver.current_url == "https://www.instagram.com/accounts/login/":
        return "login"
    elif driver.title == "Page Not Found • Instagram":
        return -2
    pre = driver.find_element_by_tag_name("pre").text
    json_data = json.loads(pre)
    if json_data == {}:
        return -2
    try:
        full_name = json_data['graphql']['user']['full_name']
        biography = json_data['graphql']['user']['biography']
        followers_count = json_data['graphql']['user']['edge_followed_by']['count']
        following_count = json_data['graphql']['user']['edge_follow']['count']
        posts_count = json_data['graphql']['user']['edge_owner_to_timeline_media']['count']
        is_private = json_data['graphql']['user']['is_private']
        return full_name, biography, followers_count, following_count, posts_count, is_private
    except:
        return -1

@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico')

@app.route("/p/<shortcode>/", methods=['GET'])
def api_post(shortcode):
    post_data = get_post_data(shortcode)
    if post_data == "login":
        data = {'message':'instagram rate limit reached'}
        response = app.response_class(response=json.dumps(data), status=500, mimetype='application/json')
    else:
        if type(post_data) == int:
            likes_counter = views_counter = post_data
        else:
            likes_counter = post_data[0]
            views_counter = post_data[1]
        data = {'shortcode':str(shortcode), 'likes_count':str(likes_counter), 'views_count':str(views_counter)}
        response = app.response_class(response=json.dumps(data, ensure_ascii=False), mimetype='application/json')
    return response

@app.route("/<username>/", methods=['GET'])
def api_user(username):
    user_data = get_user_data(username)
    if user_data == "login":
        data = {'message':'instagram rate limit reached'}
        response = app.response_class(response=json.dumps(data), status=500, mimetype='application/json')
    else:
        if type(user_data) == int:
            name = followers_counter = following_counter = posts_counter = is_private = bio = user_data
        else:
            name = user_data[0]
            bio = user_data[1]
            followers_counter = user_data[2]
            following_counter = user_data[3]
            posts_counter = user_data[4]
            is_private = user_data[5]
        data = {'username':username, 'name':str(name), 'bio':str(bio), 'followers_count':str(followers_counter), 'following_count':str(following_counter), 'posts_count':str(posts_counter), 'is_private':str(is_private)}
        response = app.response_class(response=json.dumps(data, ensure_ascii=False), mimetype='application/json')
    return response

@app.errorhandler(404)
def page_not_found(error):
    data = {'message':'not found'}
    response = app.response_class(response=json.dumps(data), status=404, mimetype='application/json')
    return response

app.run(host='0.0.0.0', port=18450)