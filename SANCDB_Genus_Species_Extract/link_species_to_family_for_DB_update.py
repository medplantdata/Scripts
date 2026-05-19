import requests
import pandas as pd
import time

# uses the GBIF API to get a family name for each species and encodes the data so it can be added to the wanddb

# quick code for one family name lookup
"""url = "https://api.gbif.org/v1/species/match"
params = {"name": "Acacia dealbata"}

r = requests.get(url, params=params, timeout=10)
r.raise_for_status()
data = r.json()

print("usageKey:", data.get("usageKey"))
print("family:", data.get("family"))"""

# full code to make dataframe and genus_species_family.csv with family names for all species in the SANCDB
db = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/genus_species_fromSANCDB.csv')
URL = "https://api.gbif.org/v1/species/match"
entry =[]

for genus, species in zip(db['genus'], db['species']):
    time.sleep(5)
    name = f"{genus} {species}"
    params = {"name": name}
    try:
        r = requests.get(URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        family = data.get("family", "NA")
    except requests.exceptions.RequestException as e:
        print(f"Error for {name}: {e}")
        family = "NA"
    entry.append((genus, species, family))
    print(f"Processed: {name} - Family: {family}")

db_family = pd.DataFrame(entry, columns=['genus', 'species', 'family'])
db_family.to_csv('genus_species_family.csv', index=False)


