# Instagram Scraping Server

Instagram Scraping Server is a simple API that returns Instagram Likes, Views or Followers counts of a given post's shortcode or profile's username, built with Python and Flask.

## Requirements

* Chrome Webdriver instance
* Some Python libraries: Selenium, Flask

## Documentation

### Get views count

**Definition**

`GET /views?shortcode=<ig_post_shortcode>`

**Response**

- `200 OK` on success
```json
{
	"shortcode": "<ig_post_shortcode>",
	"views_count": "<views_count>"
}
```

- `400/404 Not Found` on failure
```json
{
	"message": "<error>",
}
```

### Get likes count

**Definition**

`GET /likes?shortcode=<ig_post_shortcode>`

**Response**

- `200 OK` on success
```json
{
	"shortcode": "<ig_post_shortcode>",
	"likes_count": "<likes_count>"
}
```

- `400/404 Not Found` on failure
```json
{
	"message": "<error>",
}
```

### Get followers count

**Definition**

`GET /followers?username=<ig_username>`

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

### Likes/Views/Followers Count replies

- `> 0` = Actual count
- `-1` = No counter
- `-2` = Page Not Found