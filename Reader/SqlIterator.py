import os

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///SQL/database.db', echo=True)

from SQL.init_db import Addresses

# https://opencagedata.com 
# ten out of ten geolocator api

from opencage.geocoder import OpenCageGeocode

class SqlIterator():
    """
    Iterates through the data, formats locaitons, and sends it to get it geolocated, then uploads that data.
    """

    def __init__(self, debug=False, **kwargs):
        self.__setup_engine(**kwargs)
        self.__id = 0
        self.debug = debug
        key = os.environ['OPENCAGE_KEY']
        self.__geocoder = OpenCageGeocode(key)
        # THIS SHOULD ALREADY EXIST! IN THE DATA. THOMAS, PLEASE UPDATE
        self.city = 'kitchener-waterloo'

    def __iter__(self, ):
        pass

    def __next__(self, ):
        self._get_data()
        self._format_input()
        self._results = self.__geocoder.geocode(self.query)
        self._parse_response()
        self._populate_sql()

    def __setup_engine(self, **kwargs):
        if 'engine' in kwargs.keys():
            self.__Session = sessionmaker(bind=kwargs['engine'])
        else:
            engine = create_engine('sqlite:///SQL/database.db')
            self.__Session = sessionmaker(bind=engine)


    def _get_data(self):
        self.session = self.__Session()
        entry = self.session.query(Addresses).filter(and_(
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
        self.entry = entry

    def _format_input(self):
        self.query = f'{self.item["house_number"]} {self.item["street_name"]},'
        self.query += f'Toronto, ON, Canada'
        if self.debug:
            print(self.query)

    def _populate_sql(self):
        try:
            self.entry.postal_code = self.response_map['postal_code']
        except:
            pass
        try:
            self.entry.city_disctict = self.response_map['city_district']
        except:
            pass
        try:
            self.entry.latitude = self.response_map['latitude']
        except:
            pass
        try:
            self.entry.longitude = self.response_map['longitude']
        except:
            pass
        try:
            self.entry.neighbourhood = self.response_map['neighbourhood']
        except:
            pass
        try:
            self.entry.processed = 1
        except:
            pass
        print(f'{self.entry.house_number}-{self.entry.street_name}, {self.entry.neighbourhood}')
        
        self.session.commit()

    def _parse_response(self):
        if self.debug:
            print(self._results)

        self.response_map={
                'latitude':self._results[0]['geometry']['lat'],
                'longitude':self._results[0]['geometry']['lng'],
                }

        for component in ['postcode','neighbourhood','city_district']:
            try:
                component = self._results[0]['components'][component]
                if type(component) != str:
                    component=str(component)[1:-1]
                self.response_map[component] = component
            except Exception as e:
                self.response_map[component] = ''
                print(f'error with {component}'+str(e))

        if self.debug:
            print(self.response_map)


if __name__ == "__main__":
    SqlIterator()


