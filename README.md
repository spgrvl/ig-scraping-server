# Instagram Scraping Server

Instagram Scraping Server is a simple API that returns Instagram Likes or Views counts of a given post's shortcode, built with Python and Flask.

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

### Likes/Views Count replies

- `> 0` = Actual views count
- `-1` = No views counter
- `-2` = Page Not Found