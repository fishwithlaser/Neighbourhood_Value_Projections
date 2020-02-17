
import os
from SQL.tools import get_engine
from sqlalchemy.ext.declarative import declarative_base
from SQL.init_db import Addresses
from Reader.get_data import get_data

def raw_to_sql():
    #sets up SQL stuff
    engine = get_engine()
    Base = declarative_base()
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    #gets data

    file_list = os.listdir('BuildingPermits')
    
    for filename in file_list:
        data = get_data(os.path.join('BuildingPermits',filename))
         
        for datum in data:

            #semingly i dont actually get any data yet??
            Address = Addresses(
                    house_number = datum['house_number'],
                    street_name = datum['street_name'],
                    status = datum['status'],
                    city = datum['city'],
                    date_issued = datum['date_issued'],
                    date_expired = datum['date_expired'],
                    description = datum['description']
                    )
            try:
                if len(str(datum['latitude']))>0:
                    Addresses.latitude=datum['latitude']
                    Addresses.longitude=datum['longitude']
                    Addresses.status=1
            except:
                #if they don't exist then we are not done and dont set a statuse
                pass

            session.add(Address)
        #except Exception as e:
        #    print(e)
        #    print(datum)

        session.commit()
        session.close()

if __name__ == "__main__":
    raw_to_sql()
