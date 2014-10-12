
# About:

We made this as a service for a fellowship project in Mesa, AZ. Because it is based on US Government TIGER data, it might be easy to use for projects in other places. We've set up a few of them as examples.

# What it does:

Given some free form text, this tool finds geographic entities (lines, points) inside that text and returns GeoJSON.

It works by finding things in your text that look like they might be streets (substrings in the text ending in words like 'Road' or 'Street') and comparing them to actual streetnames from a TIGER database for a specific area (e.g. Mesa, Arizona).

# TODO:

Would you like to see your city in here? Please post in the "issues" section.

# Setup:

To make the API for your city, follow the database steps below.

1. Run `make database` in the root directory to build the database of local roads. This currently defaults to setting up manhattan. Set the Makefile's PLACEID to the correct ID for your place of interest in the Census Reporter (http://censusreporter.org).

  For now, you can search Census Reporter for appropriate place ID's with
    make find_place_id PLACENAME="New York, NY"

  Then, you can search for the appropriate TIGER Line ID with:
    make find_tiger_line_id

  Then you can:
    make tiger_tables TIGERID="06075" PLACEID="16000US0667000" #san francisco city

  Or you can use [Metro-Extracts](http://metro.teczno.com/) like so: (this is a little buggy now)
    make metro_tables PLACENAME="portland"

2. If on Heroku, you can also run `make database_push` to push to your heroku app.
Note that to use PostGIS extension, you'll need to get a premium level heroku postgres addon.

    heroku addons:add heroku-postgresql:premium-0

You then will want to promote the premium database to be accessed through heroku's DATABASE_URL environment variable.

    heroku pg:promote HEROKU_POSTGRESQL_YELLOW_URL

Once you've done the above you can push the table to heroku:
    make push_table_heroku TABLENAME="portland" APPNAME="yourappname"

# Table Naming:

during the make process, several tables will be created.

If you use Tiger, tables named after the Tiger ID preceded by n are street names
Those preceded by e are edges.

The table preceded by 'b' with a PLACEID is the boundary for your selected city.

The table ub(PLACEID) is the road table that is used for the main search.

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
