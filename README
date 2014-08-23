
# About:

Given some free form text, this tool finds geographic entities (lines, points) inside that text and returns GeoJSON.

It works by finding things in your text that look like they might be streets (substrings in the text ending in words like 'Road' or 'Street') and comparing them to actual streetnames from a TIGER database for a specific area (e.g. Mesa, Arizona).

# TODO:

Currently this only works in Mesa, AZ (because our street data from the Census Bureau is currently only in that area). It shouldn't be hard to make this work for other places. Pull requests welcome.


# Setup:

1. Run `make` in the data directory to build the database of local roads. If you want this to work outside of Mesa, set the Makefile's PLACEID to the correct ID for your place of interest in the Census Reporter (http://censusreporter.org).

2. If on Heroku, you can run `make database_push` to push to your heroku app.
Note that to use PostGIS extension, you'll need to get a premium level heroku postgres addon.

    heroku addons:add heroku-postgresql:premium-0

You then will want to promote the premium database to be accessed through heroku's DATABASE_URL environment variable.

    heroku pg:promote HEROKU_POSTGRESQL_YELLOW_URL

# Usage:

There's a couple ways to run the server.

1. On your development machine:

     make run_server

(or `make debug_server` for debug mode)

2. You can also start it the way Heroku will:

    gunicorn server:app

If you need to use a database other than 'tiger' on the localhost with no authentication, you can set the database url via the DATABASE_URL
environment variable.

# Testing:

Run the following command to POST some example text to the server.

	make run_test

I'd recommend using the Chrome extension 'Postman' for further testing. You'll need to pass some form data such that 'fileupload' is the key and your free form text containing addresses is the value.

