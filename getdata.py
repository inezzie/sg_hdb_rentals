import sqlite3
import requests
import json
import time

conn = sqlite3.connect('rental.sqlite')
cur = conn.cursor()

# {'_id': 1, 'block': '105', 'flat_type': '4-ROOM', 'monthly_rent': '2000', 'rent_approval_date': '2021-01', 'street_name': 'ANG MO KIO AVE 4', 'town': 'ANG MO KIO'}
# cur.execute("DROP TABLE IF EXISTS rental")
cur.executescript("""
                  CREATE TABLE IF NOT EXISTS rental (
                    id                  INTEGER UNIQUE PRIMARY KEY,
                    town                TEXT,
                    flat_type           TEXT,
                    block               TEXT,
                    street_name         TEXT,
                    location            TEXT,
                    rent_approval_date  DATE,
                    monthly_rent        FLOAT64
                  );
                  """)

animation = [" .       ", " . .     ", " . . .   ", " . . . . "]
run_count = 0
offsetCount = 0
progress = True
print_offset = False

cur.execute("SELECT COUNT(*) FROM rental")
exist_records = cur.fetchone()[0]

while progress is True:
    # Grab data using the provided open AI call.
    baseURL = "https://data.gov.sg/api/action/datastore_search?resource_id="
    datasetId = "d_c9f57187485a850908655db0e8cfe651"
    nextQuery = "&offset="
    if run_count == 0:
        url = baseURL + datasetId
    else:
        url = baseURL + datasetId + nextQuery + str(offsetCount)

    # Read response as JSON
    response = requests.get(url).json()
    rdump = json.dumps(response, sort_keys=True, indent=4)
    rdata = json.loads(rdump)
    total_records = rdata["result"]["total"]
    
    if rdata["success"] != True:
        progress = False
        print("API response failed.")
    
    if int(exist_records) == total_records:
        progress = False
        print("No new records to retrieve.")

    if run_count <= total_records:
        # Wait loading animation
        print("In Progress", animation[run_count % len(animation)], end="\r")
        time.sleep(0.3)
        run_count += 1
        
        if exist_records > 0 and exist_records < total_records and print_offset == False:
            offsetCount = exist_records - (exist_records % 100)
            if print_offset == False: print(str(offsetCount) + " existing records found. Retrieving new records.")
            print_offset = True
        else:
            offsetCount += 100
    
    if run_count % 1000 == 0 :
        print(str(run_count) + " records inserted.")
        time.sleep(0.5)
    
    if run_count >= total_records:
        progress = False
        print("No more records to retrieve.")

    records = rdata["result"]["records"]
    
    for r in records:
        block = r["block"]
        street = r["street_name"]
        loc = {'location': block + " " + street}
        r.update(loc)
    
    cur.executemany("INSERT OR IGNORE INTO rental VALUES (:_id, :town, :flat_type, :block, :street_name, :location, :rent_approval_date, :monthly_rent)", records)
    conn.commit()

cur.close()
