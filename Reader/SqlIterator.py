from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///SQL/database.db', echo=True)

from SQL.init_db import Addresses

class SqlIterator():
    """
    Iterates through the data, formats locaitons, and sends it to get it geolocated, then uploads that data.
    """

    def __init__(self, **kwargs):
        self.__setup_engine(**kwargs)
        self.__id = 0
        # THIS SHOULD ALREADY EXIST! IN THE DATA. THOMAS, PLEASE UPDATE
        self.city = 'Toronto'

    def __iter__(self, ):
        pass

    def __next__(self, ):
        self._get_data()
        self._format_input()
        #send to people

    def __setup_engine(self, **kwargs):
        if 'engine' in kwargs.keys():
            self.__Session = sessionmaker(bind=kwargs['engine'])
        else:
            engine = create_engine('sqlite:///SQL/database.db')
            self.__Session = sessionmaker(bind=engine)

    def _get_data(self):
        session = self.__Session()
        entry = session.query(Addresses).filter(and_(
                Addresses.processed == False,
                Addresses.id > self.__id)).first()
        # tracks location in iteration
        
        self.__id = entry.id
        
        self.item = {
                  'id':entry.id,
                  'house_number':entry.house_number,
                  'street_name':entry.street_name,
                  'city':entry.city,
                  'latitude':entry.latitude,
                  'longitude':entry.longitude,
                  'status':entry.status,
                  'date_issued':entry.date_issued,
                  'date_expired':entry.date_expired,
                  'description':entry.description,
                  'city_district':entry.city_district,
                  'neighbourhood':entry.neighbourhood,
                  'postal_code':entry.postal_code,
                  'procesed':entry.processed
                  }

    def _format_input(self):
        self.query = f'{self.item["house_number"]} {self.item["street_name"]}, Toronto, ON, Canada'
        print(self.query)

if __name__ == "__main__":
    SqlIterator()


