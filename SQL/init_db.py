from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///SQL/database.db')
Base = declarative_base()

class Addresses(Base):

    __tablename__ = "Addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    PID = Column(Integer)
    house_number= Column(Integer)
    street_name= Column(String)
    city= Column(String)
    latitude= Column(Integer)
    longitude= Column(Integer)
    status= Column(String)
    date_issued= Column(String)
    date_expired= Column(String)
    description= Column(String)
    city_district= Column(String)
    neighbourhood= Column(String)
    postal_code= Column(String)
    processed= Column(Boolean, default=False)

if __name__ == '__main__':
    Base.metadata.create_all(engine)

