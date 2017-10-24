# tcg-scraper

An attempt to play around with TCG's market prices.

This app saves a copy of the specified product as a local JSON file, and checks every 5 seconds if there is a change in the market value. If there is, an alert is displayed and the user is emailed of the change.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.

### Initial Setup
You'll need to follow the instructions [here](https://docs.tcgplayer.com/docs/getting-started) to get your own BEARER token and replace it within `app.py` in the `getRequest()` function.

```
"Authorization": "bearer YOUR_BEARER_TOKEN_HERE"
```

### Required software
`python 3`

### Recommended software
`postman`

Check out this [blog post](https://medium.com/@Jessepeplinski/connecting-to-tcgplayers-api-with-postman-ce459d809a54) I wrote on getting the TCG API setup with postman.

### Required packages
`requests, json`

### Running the app
`python3 app.py`

### Example run
[![asciicast](https://asciinema.org/a/143890.png)](https://asciinema.org/a/143890)

* I created this fancy GIF with [asciinema](asciinema.org). `brew install asciinema` and `asciinema rec`

### Future Implementation

Check out the planned work in the issues.

At a high level:

1. Entry of multiple product ID's
2. Create front-end with Django or Flask
    1. Subscribe to cards
    2. Subscribed cards view
    3. All cards view
3. Display low market value and high market value

## Authors

**Jesse Peplinski**
