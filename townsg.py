import sqlite3
import re
import json

conn = sqlite3.connect('rental.sqlite')
cur = conn.cursor()

run = True
fhand = open('townsg.json', 'r+')
try:
    fdata = json.load(fhand)
except:
    print("File is empty. Updating file now.")
    run = False

new_dict = {"type":"FeatureCollection","features":[]}
# Write distinct town ID and names to a JSON file
if run is False:
    cur.execute('''
                SELECT
                    ren.*,
                    loc.lon,
                    loc.lat
                FROM (
                    SELECT
                        town,
                        AVG(lon) AS lon,
                        AVG(lat) AS lat
                    FROM location
                    GROUP BY 1
                ) loc
                INNER JOIN (
                    SELECT
                        town,
                        CAST(MIN(monthly_rent) AS INT54) AS min_rent,
                        CAST(MAX(monthly_rent) AS INT54) AS max_rent,
                        IFNULL(ROUND(AVG(monthly_rent), 2), 0) AS avg_rent,
                        IFNULL(ROUND(AVG(CASE WHEN flat_type = '1-ROOM' THEN monthly_rent END), 2), 0) AS avg_rent_1room,
                        IFNULL(ROUND(AVG(CASE WHEN flat_type = '2-ROOM' THEN monthly_rent END), 2), 0) AS avg_rent_2room,
                        IFNULL(ROUND(AVG(CASE WHEN flat_type = '3-ROOM' THEN monthly_rent END), 2), 0) AS avg_rent_3room,
                        IFNULL(ROUND(AVG(CASE WHEN flat_type = '4-ROOM' THEN monthly_rent END), 2), 0) AS avg_rent_4room,
                        IFNULL(ROUND(AVG(CASE WHEN flat_type = '5-ROOM' THEN monthly_rent END), 2), 0) AS avg_rent_5room,
                        IFNULL(ROUND(AVG(CASE WHEN flat_type = 'EXECUTIVE' THEN monthly_rent END), 2), 0) AS avg_rent_executive
                    FROM rental
                    GROUP BY 1
                ) ren USING (town)
                ''')
    data = cur.fetchall()
    
    features = []
    towns = []
    for row in data:
        town = row[0]
        min_rent = row[1]
        max_rent = row[2]
        avg_rent = row[3]
        avg_rent_1room = row[4]
        avg_rent_2room = row[5]
        avg_rent_3room = row[6]
        avg_rent_4room = row[7]
        avg_rent_5room = row[8]
        avg_rent_executive = row[9]
        lon = row[10]
        lat = row[11]
        coord = [lon, lat]

        if len(town.split()) == 3: town_id = "".join(re.findall(r"\b\w{1}", town))
        if len(town.split()) == 2:
            for match in re.findall(r"^(\w{1}).*(\b\w{2})", town):
                town_id = "".join(match)
        if len(town.split()) == 1: town_id = town[:3]
        town_id = town_id.upper()
        
        value = {
                'type':'Feature',
                # 'id':town_id,
                'geometry':{'type':'Point','coordinates':coord},
                'properties':{
                    'name':town,
                    'min_rent':min_rent,
                    'max_rent':max_rent,
                    'avg_rent':avg_rent,
                    'avg_rent_1room':avg_rent_1room,
                    'avg_rent_2room':avg_rent_2room,
                    'avg_rent_3room':avg_rent_3room,
                    'avg_rent_4room':avg_rent_3room,
                    'avg_rent_5room':avg_rent_5room,
                    'avg_rent_executive':avg_rent_executive
                    }
                }
        
        features.append(value)

    new_dict['features'] = features
    js_obj = json.dumps(new_dict, indent=4)
    fhand.write(js_obj)
    run = True