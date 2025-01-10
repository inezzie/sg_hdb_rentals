import sqlite3
import re
import requests
import json
import time

conn = sqlite3.connect('rental.sqlite')
cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS location;)

cur.executescript('''
                  CREATE TABLE IF NOT EXISTS location (
                    id                  TEXT UNIQUE PRIMARY KEY,
                    town                TEXT,
                    block               TEXT,
                    street_name         TEXT,
                    location            TEXT,
                    address             TEXT,
                    lat                 FLOAT64,
                    lon                 FLOAT64
                  );
                  ''')

# Get total count of stored records
cur.execute('SELECT COUNT(*) FROM rental')
total_records = cur.fetchone()[0]

# Get total count of unique locations
cur.execute('SELECT COUNT(DISTINCT location) FROM rental')
total_location = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM location")
current_location = cur.fetchone()[0]

if current_location != total_location:
    # Update rental table to combine block and street_name fields
    streets = []

    cur.execute('''
                SELECT DISTINCT
                    town,
                    block,
                    street_name,
                    location
                FROM rental
                ORDER BY street_name, location''')
    results = cur.fetchall()

    for result in results:
        town = result[0]
        block = result[1]
        street = result[2]
        loc = result[3]
        
        # Use starting characters from street_name and running numbers to generate location ID
        loc_code = "".join(re.findall(r"\b[A-Z]", street)) + "_"
        if loc_code not in streets:
            streets.append(loc_code)
            id = 1
        else:
            id += 1
        loc_id = loc_code  + str(id)

        cur.execute("""
                    INSERT OR REPLACE INTO location
                    (id, town, block, street_name, location)
                    VALUES (?,?,?,?,?)""",
                    (loc_id, town, block, street, loc)
                    )
        conn.commit()

run_count = 0
cur.execute('SELECT id, location FROM location WHERE address IS NULL')
results = cur.fetchall()

if results:
    for result in results:
        id = result[0]
        loc = result[1]

        # Use OneMap SG to find coordinates for each location
        query = loc.replace(' ', '+').strip()
        url = "https://www.onemap.gov.sg/api/common/elastic/search?returnGeom=Y&getAddrDetails=Y&searchVal=" + query
        headers = {"Authorization": "---"}
        response = requests.request("GET", url, headers=headers)

        if response.status_code != 200:
            print("API error occurred:", response.status_code)
            break

        js = json.loads(response.text)
        address = js["results"][0]["ADDRESS"]
        lat = js["results"][0]["LATITUDE"]
        lon = js["results"][0]["LONGITUDE"]
        
        cur.execute("""UPDATE location SET address=?, lat=?, lon=? WHERE id=?""", (address, lat, lon, id))
        conn.commit()
        run_count += 1

        if run_count >= total_location or result is None:
            print("All locations retrieved.")
            break

        if run_count % 100 == 0:
            time.sleep(0.5)
        
        if run_count % 1000 == 0:
            print(run_count, "locations retrieved.")

cur.close()
