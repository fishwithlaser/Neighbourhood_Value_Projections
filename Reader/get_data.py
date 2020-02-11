def get_data(filename):
    f = open(filename, "r")
    entries = []
    last_entry = []
    f_line = True
    for line in f.readlines():    
        if f_line:
            f_line = False
            continue

        entry = last_entry+line.split(',')
        #early break due to EOL in field
        if len(entry) < 20: 
            last_entry = entry
            continue
        else:
            last_entry = []

        # they provide a bunch of stuff what I dont understand
        try:
            permit = {'PID':entry[1],
                    'house_number':int(entry[2].strip()),
                    'street_name':entry[3].strip(),
                    'lat_long':None,
                    'build_type':entry[10],
                    'status':entry[11],
                    'date_issued':entry[12],
                    'date_expired':entry[13],
                    'description':entry[15]}
            #print(f"{permit['house_number']} {permit['street_name']}")
            
        except Exception as e:
            print(e)
            permit = {}
            #print(f'Could not build map for entry {line}')

        # sometimes the desc is too many lines and messes up the rest of the parcing,
        # but we only care about the stuff before, so we discared extra fake entries
        try:
            if permit['street_name'].isupper():
                entries.append(permit)
        except Exception as e:
            print(e)
            print(entry)
    return entries


