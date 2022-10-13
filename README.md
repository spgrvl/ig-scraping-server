# Instagram Scraping Server

Instagram Scraping Server is a simple API that serves information about Instagram profiles or posts such as Likes, Views or Followers counts, built with Python and Flask.

## Requirements

* Chrome Webdriver instance
* Some Python libraries: Selenium, Flask

## How to use

Run the server.py file to start the API server.  
If you want to login to Instagram in order to avoid Instagram's rate limits for non-logged-in users, use the optional argument `--login` and you will be asked to enter your Instagram account's credentials.

## Documentation

### Get profile information

**Definition**

`GET /<ig_username>/`

**Response**

- `200 OK` on success
```json
{
	"username": "<ig_username>",
	"name": "<full_name>",
	"bio": "<biograph>",
	"followers_count": "<followers_count>",
	"following_count": "<following_count>",
	"posts_count": "<posts_count>",
	"is_private": "<is_private>"
}
```

- `400/404 Not Found` on failure
```json
{
	"message": "<error>",
}
```

### Get post information

**Definition**

`GET /p/<ig_post_shortcode>/`

**Response**

- `200 OK` on success
```json
{
	"shortcode": "<ig_post_shortcode>",
	"likes_count": "<likes_count>",
	"views_count": "<views_count>"
}
```

- `400/404 Not Found` on failure
```json
{
	"message": "<error>",
}
```

### Likes/Views/Followers Count replies

- `> 0` = Actual count
- `-1` = No counter
- `-2` = Page Not Found
