from rdkit import Chem
from rdkit.Chem import PandasTools
import pandas as pd
import requests
import time
"""
# converting sdf to csv and getting rid of unnecessary columns
sdfFile = '/home/school/masters/Scripts/ANPDB/anpdb-05-2026.sdf'

df = PandasTools.LoadSDF(sdfFile)


cleaned_df = df[['identifier', 'canonical_smiles','standard_inchi', 'standard_inchi_key', 'name', 'chemical_class', 'chemical_sub_class', 
                 'chemical_super_class','np_classifier_pathway', 'np_classifier_superclass', 'np_classifier_class', 'organisms', 'synonyms'
                 , 'cas', 'ID']].copy()

# extracting plants only to reduce size it is currently 5897

URL = "https://api.gbif.org/v1/species/match"
is_plant =[]
count = 0
errors = []
for organisms in cleaned_df['organisms']:
    organisms = organisms.split('|')
    for organism in organisms:
        time.sleep(0.5)
        count += 1
        organism = organism.strip()
        params = {"name": organism}
        try:
            r = requests.get(URL, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            kingdom = data.get("kingdom", "NA")
            print(f"{count} - Processed: {organism} - Kingdom: {kingdom}")
        except requests.exceptions.RequestException as e:
            error = f"Error for {organism}: {e}"
            errors.append(error)
            print(error)
            kingdom = "NA"
        if kingdom == "Plantae":
            is_plant.append(True)
            break
    else:
        is_plant.append(False)

cleaned_df['is_plant'] = is_plant

plants_df = cleaned_df[cleaned_df['is_plant']].drop(columns=['is_plant'])
plants_df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv', index=False)
print(errors)
"""
"""
# getting GBIF accepted name and ids for all the plants so I can make a junction table
URL = "https://api.gbif.org/v1/species/match"
df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')

def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')

organismCount = 0
for organisms in df['organisms']:
    organisms = organisms.split('|')
    for organism in organisms:
        organismCount+=1

print(f"Total organisms to process: {organismCount}")

errors = []
gbif_ids = []
gbif_accepted_names = []
count = 0
for organisms in df['organisms']:
    organisms = organisms.split('|')
    idList = ''
    nameList = ''
    for organism in organisms:
        count += 1
        organism = organism.strip()
        params = {"name": organism}
        try:
            time.sleep(0.5)
            r = requests.get(URL, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            gbif_accepted_name = data.get("scientificName", "NA")
            gbif_accepted_usagekey = data.get("acceptedUsageKey", "NA")
            gbif_usagekey = data.get("usageKey", "NA")
            print(f"{count} - Processed: {organism} - GBIF ID: {gbif_usagekey} - Accepted GBIF ID: {gbif_accepted_usagekey} - Accepted Name: {gbif_accepted_name}")
            print(progress_bar(count, organismCount))
            if gbif_accepted_usagekey is not None:
                idList += f"{gbif_accepted_usagekey}|"
                nameList += f"{gbif_accepted_name}|"
            else:
                idList += f"{gbif_usagekey}|"
                nameList += f"{organism}|"
        except requests.exceptions.RequestException as e:
            print(f"Error for {count} - {organism}: {e}")
            error = f"Error for {organism}: {e}"
            errors.append(error)
    gbif_ids.append(idList[:-1])
    gbif_accepted_names.append(nameList[:-1])

df['gbif_accepted_names'] = gbif_accepted_names
df['gbif_ids'] = gbif_ids
df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants_gbifAccepted.csv', index=False)
print(errors)
"""

# the above script takes comicaly long to run so I need to do it different and find out how to do bulk download or sum
# seeing how many plants there are there
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
organismCount = 0
for organisms in df['organisms']:
    organisms = organisms.split('|')
    for organism in organisms:
        organismCount+=1
print(f"Total organisms to process: {organismCount}")

orgSet = set()
for organisms in df['organisms']:
    organisms = organisms.split('|')
    for organism in organisms:
        orgSet.add(organism.strip())
print(f"Total unique organisms to process: {len(orgSet)}")"""

#creating a unique list with the name that gets the accepted name the family and the kingdom so i can make it plants only
# and map it to db later

df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
organisms = df['organisms'].str.split('|').explode().str.strip().unique()

URL = "https://api.gbif.org/v1/species/match"
results = []

def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')

count = 0
error = []
entry = []
for organism in organisms:
    params = {"name": organism}
    count += 1
    try:
        time.sleep(0.2)
        r = requests.get(URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        gbif_accepted_name = data.get("scientificName", "NA")
        gbif_accepted_usagekey = data.get("acceptedUsageKey", "NA")
        gbif_usagekey = data.get("usageKey", "NA")
        kingdom = data.get("kingdom", "NA")
        print(f"Processed: {organism}")
        print(progress_bar(count, len(organisms)))
        if kingdom == "Plantae":
            entry.append((organism, gbif_usagekey, gbif_accepted_usagekey, gbif_accepted_name, kingdom))
        else:
            print(f"{organism} is not a plant, skipping.")
            error.append(f"{organism} is not a plant, skipping.")
    except requests.exceptions.RequestException as e:
        print(f"Error for {organism}: {e}")
        error.append(f"Error for {organism}: {e}")

df_plants = pd.DataFrame(entry, columns=['original_name', 'gbif_id', 'gbif_accepted_id', 'gbif_accepted_name', 'kingdom'])
df_plants.to_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv', index=False)
        
print(error)