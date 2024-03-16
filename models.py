from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from database import Base

class YahooHourly(Base):

     __tablename__ = 'yahoo_types_hourly'

     id = Column(Integer, primary_key=True)
     affiliate = Column(String(25), nullable=False)
     domain = Column(String(100))
     date = Column(Date, nullable=False,index=True)
     hour = Column(Integer, nullable=False)
     partner = Column(String(100), nullable=False)
     market = Column(String(4), nullable=False)
     source_tag = Column(String(100), nullable=False)
     device = Column(String(25), nullable=False)
     type_tag = Column(String(32))
     searches = Column(Integer, nullable=False)
     bidded_clicks = Column(Integer, nullable=False)
     revenue = Column(Float, nullable=False)
     tq_score = Column(Integer, nullable=False)


