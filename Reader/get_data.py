import csv

def get_data(filename):
    f = open(filename, "r")
    good_records=0
    bad_records=0

    entries = []
    last_entry = []
    f_line = True
    
    with open (filename) as csv_file:
        spamreader = csv.reader(csv_file, delimiter=',')
        for entry in spamreader:
            #early break due to EOL in field
            if len(entry) < 20: 
                last_entry = entry
                continue
            else:
                last_entry = []
            # they provide a bunch of stuff what I dont understand
        
            if 'Cambridge' in str(filename):
                permit = insert_cambridge(entry)
            elif 'Kitchener' in str(filename):
                permit = insert_kitchener(entry) 
            # the parsing can mess us due to EOL lines in the incoming data
            if 'street_name' in permit.keys():
                if permit['street_name'].isupper():
                    entries.append(permit)
                good_records += 1
            else:
                bad_records += 1
                continue
        print(f'{filename} - good records: {good_records}, bad records = {bad_records}')
    return entries

def insert_cambridge(entry):
    'parsing for cambridge'
    try:
        permit = {'PID':entry[1],
                'house_number':int(entry[2].strip()),
                'street_name':entry[3].strip(),
                'city': 'Cambridge',
                'latitude':None,
                'longitude':None,
                'build_type':entry[10],
                'status':entry[11],
                'date_issued':entry[12],
                'date_expired':entry[13],
                'description':entry[15]}
    except Exception as e:
        #print(e)
        permit = {}
    
    return permit

def insert_kitchener(entry):
    'parsing for kitchener'
    house_list = entry[9].split(' ')
    house_num = house_list [0]
    street_name = ' '.join(house_list[1:])
    desc = entry[6] + '|' + entry[10] + '|' + entry[22]  + '| contractor:'+ entry[40]
    build_type = entry[7]+  '|' + entry[20] + ':' +entry[21] + '| val: ' + entry[34]
    try:
        permit = {
                'house_number':int(house_num),
                'street_name':street_name,
                'city': 'Kitchener',
                'latitude':entry[0],
                'longitude':entry[1],
                'build_type':entry[7],
                'status':entry[11],
                'date_issued':entry[14],
                'date_expired':entry[16],
                'description':desc}
    except Exception as e:
        #print(e)
        permit = {}
    
    return permit



if __name__ == "__main__":
    import os
    for filename in os.listdir('BuildingPermits'):
        get_data(os.path.join('BuildingPermits',filename))
