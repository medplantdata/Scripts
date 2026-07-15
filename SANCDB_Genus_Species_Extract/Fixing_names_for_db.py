import requests
import pandas as pd
import time

"""df = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/old_not_correct/SANCDB_plants_for_DB.csv')
URL = "https://api.gbif.org/v1/species/match"
entry = []

for genus, species in df[['genus', 'species']].values:
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
        new_species = data.get("species", None)
        new_genus = data.get("genus", None)
        accepted_usageKey = data.get("acceptedUsageKey", None)
        acceptedScientificName = data.get("acceptedScientificName", None)
        if acceptedScientificName is None:
            acceptedScientificName = name
    except requests.exceptions.RequestException as e:
        print(f"Error for {name}: {e}")
    entry.append((new_genus, new_species, family, kingdom, usageKey, accepted_usageKey, acceptedScientificName))
    print(f"Processed: {name} - Family: {family} - Kingdom: {kingdom}")


fixed = pd.DataFrame(entry, columns=['genus', 'species', 'family', 'kingdom', 'usageKey', 'acceptedUsageKey', 'acceptedScientificName'])
fixed.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/fixed_SANCDB_plants_all_fields.csv', index=False)
"""

# quick gbif json format return check
"""URL = "https://api.gbif.org/v1/species/match"
name = "Acacia karoo"
params = {"name": name}
r = requests.get(URL, params=params, timeout=10)
r.raise_for_status()
data = r.json()

print(data)"""

"""family_ids = []"""


# now making the db export
"""df = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/fixed_SANCDB_plants_all_fields.csv')
families = pd.read_csv('APG_IV/data-apg4-master/families.csv')

for family in df['family']:
    if family not in families['family'].values:
        print(f"Family {family} not found in APG IV families list.")
    else:
        family_id = families.loc[families['family'] == family, 'family_id'].values[0]
        family_ids.append(family_id)

df['family_id'] = family_ids

entries = []
count = 19940
for genus, species, family_id, usageKey, accepted_usageKey, acceptedScientificName in df[['genus', 'species', 'family_id', 'usageKey', 'acceptedUsageKey', 'acceptedScientificName']].values:
    if pd.notna(species):
        count+=1
        new_genus = species.split()[0]
        new_species = species.split()[1]
        if pd.notna(accepted_usageKey):
            gbif_key = accepted_usageKey
        else:
            gbif_key = usageKey
        if acceptedScientificName == (genus + " " + species):
            synonym = None
        else:
            synonym = acceptedScientificName
        entries.append((count, new_genus, new_species, gbif_key, synonym, family_id))

for_db = pd.DataFrame(entries, columns=['plant_id','genus','species','gbif_key','synonyms', 'family_id'])
for_db.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/final_SANCDB_plants_for_DB.csv', index=False)"""

# removing dups in the ANPDB

anpdb = pd.read_csv('/home/school/masters/Scripts/ANPDB/plants_to_send_to_db.csv')
sancdb = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/final_SANCDB_plants_for_DB.csv')
count = 0

entry = []
for plant_id, genus, species, gbif_key, synonyms, family_id in sancdb[['plant_id','genus','species','gbif_key','synonyms', 'family_id']].values:
    if gbif_key in anpdb['gbif_key'].values:
        print(f"Duplicate found for {genus} {species} with GBIF key {gbif_key}. Skipping entry.")
    else:
        entry.append([plant_id, genus, species, gbif_key, synonyms, family_id])



df = pd.DataFrame(entry, columns=['plant_id','genus','species','gbif_key','synonyms', 'family_id'])
df = df.drop(columns=['plant_id'])

count = 19940
counts = []
for species in df['species'].values:
    count += 1
    counts.append(count)

df['plant_id'] = counts
ordered = ['plant_id','genus','species','gbif_key','synonyms', 'family_id']
df = df[ordered]


entry = []
for plant_id, genus, species, gbif_key, synonyms, family_id in df[['plant_id','genus','species','gbif_key','synonyms', 'family_id']].values:
    name = f"{genus} {species}"
    if name == synonyms:
        synonyms = ''
    gbif_key = int(gbif_key)
    entry.append([plant_id, genus, species, gbif_key, synonyms, family_id])


df = pd.DataFrame(entry, columns=['plant_id','genus','species','gbif_key','synonyms', 'family_id'])


df.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/use_final_SANCDB_plants_for_DB_no_dups.csv', index=False)
        
    