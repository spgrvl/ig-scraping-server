# Instagram Scraping Server

Instagram Scraping Server is a simple API that serves information about Instagram profiles or posts such as Likes, Views or Followers counts, built with Python and Flask.

## Requirements

* Chrome Webdriver instance
* Some Python libraries: Selenium, Flask

## Documentation

### Get profile information

**Definition**

`GET /<ig_username>/`

**Response**

- `200 OK` on success
```json
{
	"username": "<ig_username>",
	"followers_count": "<followers_count>"
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