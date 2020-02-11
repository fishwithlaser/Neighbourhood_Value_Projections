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
    print('getting data')
    #gets data
    data = get_data('BuildingPermits/Kitchener.csv')
    try: 
        for datum in data:
            Address = Addresses(
                    PID = int(datum['PID']),
                    house_number = int(datum['house_number']),
                    street_name = datum['street_name'],
                    lat_long = datum['lat_long'],
                    status = datum['status'],
                    date_issued = datum['date_issued'],
                    date_expired = datum['date_expired'],
                    description = datum['description']
                    )
            session.add(Address)
    except Exception as e:
        print(e)
        print(datum)

    session.commit()
    session.close()

if __name__ == "__main__":
    raw_to_sql()
