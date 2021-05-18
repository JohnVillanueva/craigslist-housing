# SF Craigslist Apartment Hunting Companion

For prospective San Francisco renters, or current SF renters looking to relocate within the city - this apartment pricing dashboard helps users compare aggregate pricing statistics by SF neighborhood for apartments currently listed for lease on Craigslist. Know exactly how apartment prices compare against other availabilities in the neighborhood, and from neighborhood to neighborhood.

![]('dashboardmap.jpeg')

This dashboard is built using the Python libraries Dash and Plotly Express that read from a remote MongoDB Atlas database using PyMongo. Scrapy, Scrapyd (Scrapy Daemon), and the MongoEngine ODM are also used to scrape data from Craigslist and write to MongoDB on a daily, scheduled basis.

Dashboard Application:
- Dash
- Plotly Express, MapBox
- PyMongo

Scraper:
- Scrapy
- Scrapyd, ScrapydWeb, Scrapyd-Client
- MonogoEngine
- Data Cleaning: BeautifulSoup4, RapidFuzz

Planned Updates:
- Add a Price Slider to filter by the users price range.
- Host Dash App on Heroku
