# SF Craigslist Apartment Hunting Companion

For prospective San Francisco renters, or current SF renters looking to relocate within the city - this apartment pricing dashboard helps users compare aggregate pricing statistics by SF neighborhood for apartments currently listed for lease on Craigslist. Know exactly how apartment prices compare against other availabilities in the neighborhood, and from neighborhood to neighborhood.

[Craigslist SF Apartment Hunting Companion](http://craigslist-dash.herokuapp.com/)

This dashboard is built using the Python libraries Dash and Plotly Express that read from a remote Heroku hosted Postgres database using SQLAlchemy. Scrapy and Scrapyd (Scrapy Daemon) are also used to scrape data from Craigslist and write to Postgres from a remote Heroku server.

Dashboard Application:
- Dash
- Plotly Express, MapBox
- SQLAlchemy

Scraper:
- Scrapy
- Scrapyd, ScrapydWeb, Scrapyd-Client
- SQLAlchemy
- Data Cleaning: BeautifulSoup4, RapidFuzz

Planned Updates:
- Awaiting [Pull Request #185](https://github.com/my8100/scrapydweb/pull/185) to allow single a database use on scraper server. This will allow daily automatic scrapy crawls. Currently, scrapy crawls must be manually triggered.
