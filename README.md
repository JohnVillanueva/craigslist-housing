# SF Craigslist Apartment Hunting Companion

For prospective San Francisco renters, or current SF renters looking to relocate within the city - this apartment pricing dashboard helps users compare aggregate pricing statistics by SF neighborhood for apartments currently listed for lease on Craigslist. Know exactly how apartment prices compare against other availabilities in the neighborhood, and from neighborhood to neighborhood.

![]('dashboardmap.jpeg')

This proof of concept dashboard is built using Python libraries Dash and Plotly Express that pull from a local SQLlite database using the SQLalchemy ORM. Scrapy and SQLAlchemy are also used to scrape data from Craiglist and load the data directly into the SQLite database.

Libraries and Packages:
- Dash
- Plotly Express, MapBox
- SQLAlchemy, SQLite
- Scrapy

Planned Updates:
- Data Cleaning: Relabeling improper neighborhood names consolidating into proper neighborhood. Use Word2Vec model and place with the most similar 'real' neighborhood. Overkill Strategy: Create 'lat-long' clusters from high count (i.e. real) neighborhood labels and place low count neighborhood-labeled apartments in the closest 'real' neighborhood.
- Add a Price Slider to filter by the users price range.
- Setup a cloud based MySQL or MongoDB database.
- Automate Scrapy scraper using Scrapyd
- Host Dash App on Heroku
