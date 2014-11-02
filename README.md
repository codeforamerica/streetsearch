
# StreetSearch [![Code Climate](https://codeclimate.com/github/codeforamerica/streetsearch/badges/gpa.svg)][codeclimate]

[codeclimate]: https://codeclimate.com/github/codeforamerica/streetsearch

We made this as a service for a fellowship project in Mesa, Arizona, to solve the problem of finding locations mentioned inside unstructured text ("Let's eat at Republic Empanada at **204 E 1st Ave**, ok?" or "The city's **Main Street** lightrail extension will be done in 2015.") Because it is based on US Government TIGER data, it might be easy to use for projects in other places. We've set up a few of them as examples at [streetsear.ch](http://streetsear.ch).

# What it does:

Given some free form text, this tool finds geographic entities (lines, points) inside that text and returns GeoJSON.

It works by finding things in your text that look like they might be streets (substrings in the text ending in words like 'Road' or 'Street') and comparing them to actual streetnames from a TIGER database for a specific area (e.g. Mesa, Arizona).

![Demo of StreetSearch](http://cdn.makeagif.com/media/10-26-2014/fqZltC.gif)

# TODO:

Would you like to see your city in here? Please [let us know](https://github.com/codeforamerica/streetsearch/issues/new).

# Setup:

To make the API for your city, follow the database steps below.

1. Run `make database` in the root directory to build the database of local roads. This currently defaults to setting up manhattan. Set the Makefile's PLACEID to the correct ID for your place of interest in the Census Reporter (http://censusreporter.org).

  For now, you can search Census Reporter for appropriate place ID's with
  
      $ make find_place_id PLACENAME="San Francisco, CA"
      
  Near the bottom of the output, you'll see something like this:
  
  ```json
  "results": [
    {
      "sumlevel": "160",
      "full_geoid": "16000US0667000",
      "full_name": "San Francisco, CA"
    },
    {
      "sumlevel": "060",
      "full_geoid": "06000US0607592790",
      "full_name": "San Francisco CCD, San Francisco County, CA"
    }
  ]
  ```
  
  There are multiple results in this case, but the first one (for the exact match, "San Francisco, CA") is what we want, and from here on, the value of `full_geoid` will be passed into make targets as `PLACEID`.

  Next, you can search for the appropriate TIGER Line ID like this (we're using PLACEID found above for San Francisco here):
  
      $ make find_tiger_line_id PLACEID="16000US0667000"

  The output from that command will contain a `geoid` property, and the last part of that number will be used as `TIGERID` from here on.
  
  Then you can:
  
      $ make tiger_tables TIGERID="06075" PLACEID="16000US0667000" #again, this is san francisco city

  Or you can use [Metro-Extracts](http://metro.teczno.com/) like so: (this is a little buggy now)
  
      $ make metro_tables PLACENAME="portland"

2. If on Heroku, you can also run `make database_push` to push to your heroku app. 

  Note that to use PostGIS extension, you'll need to get a premium level heroku postgres addon: 
   
      $ heroku addons:add heroku-postgresql:premium-0

You then will want to promote the premium database to be accessed through heroku's `DATABASE_URL` environment variable.

    $ heroku pg:promote HEROKU_POSTGRESQL_YELLOW_URL

Once you've done the above you can push the table to heroku:

    $ make push_table_heroku TABLENAME="portland" APPNAME="your-heroku-app-name"

# Table Naming:

during the make process, several tables will be created.

If you use Tiger, tables named after the Tiger ID preceded by `n` are street names
Those preceded by `e` are edges.

The table preceded by `b` with a `PLACEID` is the boundary for your selected city.

The table `ub(PLACEID)` is the road table that is used for the main search.

# Usage:

There's a couple ways to run the server.

1. On your development machine, run: `make run_server`

   (or run `make debug_server` for debug mode)

2. You can also start it the way Heroku will by running: `gunicorn server:app`

If you need to use a database other than `tiger` on the localhost with no authentication, you can set the database url via the `DATABASE_URL` environment variable.

# Testing:

Run the following command to POST some example text to the server.

	 $ make run_test

I'd recommend using the Chrome extension 'Postman' for further testing. You'll need to pass some form data such that 'sentence' is a key and your free form text containing addresses is the corresponding value, while 'placename' is a key and the value is "nyc", "mesa", "sf", or one of the other values expected by the geocode_text method in geocoder.py.
