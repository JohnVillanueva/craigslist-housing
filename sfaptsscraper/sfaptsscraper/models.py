import datetime
import mongoengine
from mongoengine import DateTimeField, StringField, FloatField, ObjectIdField, IntField
from scrapy.utils.project import get_project_settings

URI = get_project_settings().get('CONNECTION_STRING')
mongoengine.connect(host=URI)

class Apartment(mongoengine.Document):
    postid = IntField()
    name = StringField()
    price = FloatField()
    address = StringField()
    neighborhood = StringField()
    bedrooms = IntField()
    bathrooms = FloatField()
    link = StringField()
    postdate = DateTimeField()
    latitude = FloatField()
    longitude = FloatField()
    scrapedate = DateTimeField(default=datetime.datetime.now)






# from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import (Integer, String, Date, DateTime, Float, Boolean, Text)
# from scrapy.utils.project import get_project_settings

# #from .settings import CONNECTION_STRING

# Base = declarative_base()

# def db_connect():
#     return create_engine(get_project_settings().get('CONNECTION_STRING'))

# def create_table(engine):
#     Base.metadata.create_all(engine)

# class Apartment(Base):
#     __tablename__ = "apartment"

#     postid = Column(Integer, primary_key = True)
#     name = Column('name', Text())
#     price = Column('price', Integer)
#     address = Column('address', Text())
#     neighborhood = Column('neighborhood', Text())
#     bedrooms = Column('bedrooms', Integer)
#     bathrooms = Column('bathrooms', Float)
#     link = Column('link', Text())
#     postdate = Column('postdate', DateTime)
#     latitude = Column('latitude', Float)
#     longitude = Column('longitude', Float)