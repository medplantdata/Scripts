from typing_extensions import final

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
"""db = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/genus_species_fromSANCDB.csv')
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
db_family.to_csv('genus_species_family.csv', index=False)"""

# checking to see if the family names assigned by gbif are the same as the family names in the SANCDB
# found out there are alot of marine things there
"""dbsa = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/genus_species_family.csv')
dbapg = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/families.csv')

for family in dbsa['family'].unique():
    if family not in dbapg['family'].values:
        print(f"Family {family} not found in APG IV list.")"""

# assining kingdoms so all non plants can be removed from the SANCDB 
"""db = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/genus_species_fromSANCDB.csv')
URL = "https://api.gbif.org/v1/species/match"
entry =[]

for genus, species in zip(db['genus'], db['species']):
    time.sleep(1)
    name = f"{genus} {species}"
    params = {"name": name}
    try:
        r = requests.get(URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        family = data.get("family", "NA")
        kingdom = data.get("kingdom", "NA")
    except requests.exceptions.RequestException as e:
        print(f"Error for {name}: {e}")
        family = "NA"
        kingdom = "NA"
    entry.append((genus, species, family, kingdom))
    print(f"Processed: {name} - Family: {family} - Kingdom: {kingdom}")

db_family_kingdom = pd.DataFrame(entry, columns=['genus', 'species', 'family', 'kingdom'])
db_plants = db_family_kingdom[db_family_kingdom['kingdom'] == 'Plantae']
db_plants.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_species_genus_family_kingdom.csv', index=False)
"""
"""# Checking against APG 4 again
dbsa = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_species_genus_family_kingdom.csv')
dbapg = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/families.csv')

for family in dbsa['family'].unique():
    if family not in dbapg['family'].values:
        print(f"Family {family} not found in APG IV list.")
"""

# removing NAN and non angiosperms and the Ximenia caffra and then storing it as the same file

"""db = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_species_genus_family_kingdom.csv')
db_drop = db.dropna(subset=['family'])

nonangiosperms = ['Dumortieraceae','Marchantiaceae','Rhodomelaceae','Plocamiaceae', 'Ricciaceae','Ximeniaceae'] # ximeniacea is weird it is not in APG4 so jsut removing it which removes one entry the Ximenia caffra

db_final = db_drop[~db_drop['family'].isin(nonangiosperms)]
db_final.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_species_genus_family_kingdom.csv', index=False)
"""

#removing duplicates for genus and species
"""db = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_species_genus_family_kingdom.csv')
dups = db.duplicated(subset=['genus', 'species'], keep=False)
duplicates = db[dups]
print("Duplicate entries based on genus and species:")
print(duplicates)
db_unique = db.drop_duplicates(subset=['genus', 'species'])
db_unique.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_species_genus_family_kingdom.csv', index=False)
"""
# by using the GBIF to look for the usagekey accepted usage key and getting the officail name I will depuplicate the list for synonyms into the file offical_deduplicated_SANCDB_plants.csv
"""db = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_species_genus_family_kingdom.csv')
URL = "https://api.gbif.org/v1/species/match"
entry =[]

for genus, species in zip(db['genus'], db['species']):
    time.sleep(0.25)
    name = f"{genus} {species}"
    params = {"name": name}
    try:
        r = requests.get(URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        family = data.get("family", "NA")
        kingdom = data.get("kingdom", "NA")
        usageKey = data.get("usageKey", None)
        accepted_usageKey = data.get("acceptedUsageKey", None)
        acceptedScientificName = data.get("acceptedScientificName", None)
        if acceptedScientificName is None:
            acceptedScientificName = name
    except requests.exceptions.RequestException as e:
        print(f"Error for {name}: {e}")
        family = "NA"
        kingdom = "NA"
    entry.append((genus, species, family, kingdom, usageKey, accepted_usageKey, acceptedScientificName))
    print(f"Processed: {name} - Family: {family} - Kingdom: {kingdom}")

db_with_dup = pd.DataFrame(entry, columns=['genus', 'species', 'family', 'kingdom', 'usageKey', 'acceptedUsageKey', 'acceptedScientificName'])

db_with_dup['final_usageKey'] = db_with_dup['acceptedUsageKey'].fillna(db_with_dup['usageKey'])

db_no_dup = db_with_dup.drop_duplicates(subset=['final_usageKey'])

final = []

for scientific_name, final_usageKey, family in zip(db_no_dup['acceptedScientificName'], db_no_dup['final_usageKey'],db_no_dup['family']):
    Genus = scientific_name.split()[0]
    Species = scientific_name.split()[1]
    final.append((Genus, Species, final_usageKey, family))

db_final = pd.DataFrame(final, columns=['genus', 'species', 'usageKey', 'family' ])

db_final.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/offical_deduplicated_SANCDB_plants.csv', index=False)
"""

# making plants ready for the database
"""db = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/offical_deduplicated_SANCDB_plants.csv')
families = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/families.csv')
entry = []
count = 0

for genus,species,GBIF_usageKey, family in zip(db['genus'], db['species'], db['usageKey'], db['family']):
    count += 1
    wand_id = "p"+str(count)
    if family in families['family'].values:
        family_id = families[families['family'] == family]['family_id'].values[0]
        entry.append((wand_id,genus, species, GBIF_usageKey, family_id))
    else:
        print(f"Family {family} not found in APG IV list for {genus} {species} with GBIF usageKey {GBIF_usageKey}.")
        entry.append((wand_id,genus, species, GBIF_usageKey, family_id))

db_final = pd.DataFrame(entry, columns=['wand_id', 'genus', 'species', 'gbif_usagekey', 'family_id'])
db_final.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_for_DB.csv', index=False)
"""

