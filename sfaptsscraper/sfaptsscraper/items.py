# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
from datetime import datetime
from .neighborhoods import Neighborhood_Relabel

def remove_currency(value):
    return int(float(value.replace('$','').replace(',','').strip()))

def remove_postid(value):
    return int(value.replace('post id: ','').strip())

def convert_datetime(value):
    formatted_str = str(value)[:19].replace('T',' ')
    return datetime.strptime(formatted_str, '%Y-%m-%d %H:%M:%S')

def edit_bedroom(value):
    return int(value.replace('BR',''))

def edit_bathroom(value):
    stripped = value.replace('Ba','')
    try:
        return float(stripped)
    except:
        return float(1)

def edit_neighborhood(value):
    return value.strip()[1:-1]


class SfaptsscraperItem(scrapy.Item):
    # define the fields for your item here like:
    
    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_currency), output_processor = TakeFirst())
    address = scrapy.Field(output_processor = TakeFirst())
    neighborhood = scrapy.Field(input_processor= MapCompose(edit_neighborhood, Neighborhood_Relabel), output_processor = TakeFirst())
    bedrooms = scrapy.Field(input_processor = MapCompose(edit_bedroom), output_processor = TakeFirst())
    bathrooms = scrapy.Field(input_processor = MapCompose(edit_bathroom), output_processor = TakeFirst())
    link = scrapy.Field(output_processor = TakeFirst())
    postid = scrapy.Field(input_processor = MapCompose(remove_postid), output_processor = TakeFirst())
    postdate = scrapy.Field(input_processor = MapCompose(convert_datetime), output_processor = TakeFirst())
    latitude = scrapy.Field(input_processor = MapCompose(float), output_processor = TakeFirst())
    longitude = scrapy.Field(input_processor = MapCompose(float), output_processor = TakeFirst())
    
    pass
