# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from .models import Apartment, db_connect, create_table

# # refactoring script for mongoengine
# import mongoengine
# from scrapy.utils.project import get_project_settings

#required libraries for clearing the database table upon starting the crawl
from sqlalchemy import inspect
from sqlalchemy import create_engine, text
from scrapy.utils.project import get_project_settings
#from sqlalchemy_utils.functions import database_exists


class SfaptsscraperPipeline:

    def __init__(self):
        
        # URI = get_project_settings().get('CONNECTION_STRING')
        # mongoengine.connect(host=URI)
        # Apartment()
        # Apartment.objects.delete()
        
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        
        # Added block to clear the sfapts.db 'apartment' table upon recrawl. SQLAlchemy Implementation
        engine = create_engine(get_project_settings().get('CONNECTION_STRING'))
        if inspect(engine).has_table('apartment'):
            with engine.connect() as connection:
                connection.execute(text("DELETE FROM apartment"))
        
        # if database_exists(get_project_settings().get('CONNECTION_STRING')):
        #     engine = create_engine(get_project_settings().get('CONNECTION_STRING'))
        #     with engine.connect() as connection:
        #         connection.execute(text("DELETE FROM apartments"))
        #         #print("***apartment table cleared in sfapts.db***")

    def process_item(self, item, spider):
        
        session = self.Session()
        apartment = Apartment()

        apartment.postid = item['postid']
        apartment.name = item['name']
        apartment.price = item['price']
        apartment.address = item['address']
        apartment.neighborhood = item['neighborhood']
        apartment.bedrooms = item['bedrooms']
        apartment.bathrooms = item['bathrooms']
        apartment.link = item['link']
        apartment.postdate = item['postdate']
        apartment.latitude = item['latitude']
        apartment.longitude = item['longitude']

        #apartment.save() #mongoDB functionality

        session.add(apartment)
        session.commit()
        session.close()

        return item