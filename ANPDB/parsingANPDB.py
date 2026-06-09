from rdkit import Chem
from rdkit.Chem import PandasTools
import pandas as pd
import requests
import time
import pubchempy as pcp

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

"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
organisms = df['organisms'].str.split('|').explode().str.strip().unique()

URL = "https://api.gbif.org/v1/species/match"
results = []

def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')
nonplants = []
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
            nonplants.append(organism)
    except requests.exceptions.RequestException as e:
        print(f"Error for {organism}: {e}")
        error.append(f"Error for {organism}: {e}")

df_plants = pd.DataFrame(entry, columns=['original_name', 'gbif_id', 'gbif_accepted_id', 'gbif_accepted_name', 'kingdom'])
df_plants.to_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv', index=False)
df_nonplants = pd.DataFrame(nonplants, columns=['non_plant_organisms'])
df_nonplants.to_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv', index=False)
print(error)"""

# The total number of organisms is more than the plant and non plant organisms so this code is to try see what was missing

"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
organisms = df['organisms'].str.split('|').explode().str.strip().unique()
df_plants = pd.read_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv')
df_nonplants = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

missing_organisms = set(organisms) - set(df_plants['original_name']) - set(df_nonplants['non_plant_organisms'])
print(f"Total missing organisms: {len(missing_organisms)}")
print(f"Missing organisms: {', '.join(missing_organisms)}")
for organism in missing_organisms:
    print(organism)"""


# querying the GBIF to see what was wrong with these organisms
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
organisms = df['organisms'].str.split('|').explode().str.strip().unique()
df_plants = pd.read_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv')
df_nonplants = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

missing_organisms = set(organisms) - set(df_plants['original_name']) - set(df_nonplants['non_plant_organisms'])

newMissing_organisms = []
URL = "https://api.gbif.org/v1/species/match"
for organism in missing_organisms:
    params = {"name": organism}
    try:
        time.sleep(0.1)
        r = requests.get(URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        gbif_accepted_name = data.get("scientificName", "NA")
        gbif_accepted_usagekey = data.get("acceptedUsageKey", "NA")
        gbif_usagekey = data.get("usageKey", "NA")
        kingdom = data.get("kingdom", "NA")
        print(f"Processed: {organism} - GBIF ID: {gbif_usagekey} - Accepted GBIF ID: {gbif_accepted_usagekey} - Accepted Name: {gbif_accepted_name} - Kingdom: {kingdom}")
        newMissing_organisms.append((organism, gbif_usagekey, gbif_accepted_usagekey, gbif_accepted_name, kingdom))
    except requests.exceptions.RequestException as e:
        print(f"Error for {organism}: {e}")

df_missing = pd.DataFrame(newMissing_organisms, columns=['original_name', 'gbif_id', 'gbif_accepted_id', 'gbif_accepted_name', 'kingdom'])
print(df_missing.shape)"""



# adding the missing organisms to the plants and non plants csvs and pulling out the weird ones
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
organisms = df['organisms'].str.split('|').explode().str.strip().unique()
df_plants = pd.read_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv')
df_nonplants = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

missing_organisms = set(organisms) - set(df_plants['original_name']) - set(df_nonplants['non_plant_organisms'])

new_plants = []
new_nonplants = []
nowhere = []

URL = "https://api.gbif.org/v1/species/match"
for organism in missing_organisms:
    params = {"name": organism}
    try:
        time.sleep(0.1)
        r = requests.get(URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        gbif_accepted_name = data.get("scientificName", "NA")
        gbif_accepted_usagekey = data.get("acceptedUsageKey", "NA")
        gbif_usagekey = data.get("usageKey", "NA")
        kingdom = data.get("kingdom", "NA")
        print(f"Processed: {organism} - GBIF ID: {gbif_usagekey} - Accepted GBIF ID: {gbif_accepted_usagekey} - Accepted Name: {gbif_accepted_name} - Kingdom: {kingdom}")
        if kingdom == "Plantae":
            new_plants.append((organism, gbif_usagekey, gbif_accepted_usagekey, gbif_accepted_name, kingdom))
        elif kingdom == "NA":
            nowhere.append((organism, gbif_usagekey, gbif_accepted_usagekey, gbif_accepted_name, kingdom))
        else:
            new_nonplants.append((organism, gbif_usagekey, gbif_accepted_usagekey, gbif_accepted_name, kingdom))
    except requests.exceptions.RequestException as e:
        print(f"Error for {organism}: {e}")

df_new_plants = pd.DataFrame(new_plants, columns=['original_name', 'gbif_id', 'gbif_accepted_id', 'gbif_accepted_name', 'kingdom'])
df_new_nonplants = pd.DataFrame(new_nonplants, columns=['original_name')
df_nowhere = pd.DataFrame(nowhere, columns=['original_name', 'gbif_id', 'gbif_accepted_id', 'gbif_accepted_name', 'kingdom'])

df_plants = pd.concat([df_plants, df_new_plants], ignore_index=True)
df_nonplants = pd.concat([df_nonplants, df_new_nonplants], ignore_index=True)

df_plants.to_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv', index=False)
df_nonplants.to_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv', index=False)
df_nowhere.to_csv('/home/school/masters/Scripts/ANPDB/nowhere_organisms.csv', index=False)
print(df_nowhere)"""

# previous run had 2 errors rechecking the left out 
"""
df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
organisms = df['organisms'].str.split('|').explode().str.strip().unique()
df_plants = pd.read_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv')
df_nonplants = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

missing_organisms = set(organisms) - set(df_plants['original_name']) - set(df_nonplants['non_plant_organisms'])

print(f"Total missing organisms: {len(missing_organisms)}")
print(f"Missing organisms: {', '.join(missing_organisms)}")
"""

# fixing a fuck up with the concatenation
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

df.drop(columns=['gbif_id', 'gbif_accepted_id', 'gbif_accepted_name', 'kingdom'], inplace=True)

df['non_plant_organisms'] = df['non_plant_organisms'].fillna(df['original_name'])

df.drop(columns=['original_name'], inplace=True)

df.to_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv', index=False)"""

# deleting non distinct from non plants
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

df.drop_duplicates(subset=['non_plant_organisms'], inplace=True)

df.to_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv', index=False)"""

# something is weird here 
"""
df = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

print(df.shape)"""

# manually adding weird entries
"""missing_og_names = ['Santalum Album', 'Eugenia sp.', 'Phaseolus Vulgaris', 'Morinda Citrifolia', 'Datura Innoxia', 'Herreania sp.']
manual_corrections = ['Santalum album', 'Eugenia spp.', 'Phaseolus vulgaris', 'Morinda citrifolia', 'Datura innoxia', 'Herreania spp.']
df_plants = pd.read_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv')
df_nonplants = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

url = "https://api.gbif.org/v1/species/match"

new_plants = []
new_nonplants = []

for og_name, corrected_name in zip(missing_og_names, manual_corrections):
    params = {"name": corrected_name}
    try:
        time.sleep(0.1)
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        gbif_accepted_name = data.get("scientificName", "NA")
        gbif_accepted_usagekey = data.get("acceptedUsageKey", "NA")
        gbif_usagekey = data.get("usageKey", "NA")
        kingdom = data.get("kingdom", "NA")
        print(f"Processed: {corrected_name} - GBIF ID: {gbif_usagekey} - Accepted GBIF ID: {gbif_accepted_usagekey} - Accepted Name: {gbif_accepted_name} - Kingdom: {kingdom}")
        if kingdom == "Plantae":
            new_plants.append({'original_name': og_name, 'gbif_id': gbif_usagekey, 'gbif_accepted_id': gbif_accepted_usagekey, 'gbif_accepted_name': gbif_accepted_name, 'kingdom': kingdom})
        else:
            new_nonplants.append({'non_plant_organisms': og_name})
    except requests.exceptions.RequestException as e:
        print(f"Error for {corrected_name}: {e}")

df_plants = pd.concat([df_plants, pd.DataFrame(new_plants)], ignore_index=True)
df_nonplants = pd.concat([df_nonplants, pd.DataFrame(new_nonplants)], ignore_index=True)

df_plants.to_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv', index=False)
df_nonplants.to_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv', index=False)"""

# removing all of the non plants from the csv 

"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
df_nonplants = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')
nonplant_set = set(df_nonplants['non_plant_organisms'].str.strip())
def return_plant_list(organisms):
    out = ''
    for organism in organisms.split('|'):
        if organism.strip() not in nonplant_set:
            out += f"{organism.strip()}|"
    if out == '':
        out = 'no_plants|'
    return out[:-1]


df['organisms'] = df['organisms'].apply(return_plant_list)

df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv', index=False)

count = 0
for organisms in df['organisms']:
    if organisms == 'no_plants':
        count += 1
        print(organisms)
print(f"Total no_plants entries: {count}")"""

# double checking that all the no_plants entries are gone and that the plants csv is correct
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
plant_db = pd.read_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv')
nonplant_db = pd.read_csv('/home/school/masters/Scripts/ANPDB/non_plant_organisms.csv')

plant_set = set(plant_db['original_name'].str.strip())
nonplant_set = set(nonplant_db['non_plant_organisms'].str.strip())

for organisms in df['organisms']:
    for organism in organisms.split('|'):
        if organism.strip() not in plant_set and organism.strip() not in nonplant_set:
            print(f"Organism not found in either set: {organism.strip()}")
        
        if organism.strip() in nonplant_set:
            print(f"there is an imposter among us: {organism.strip()}")"""

# creating the CSV for compound to DB export
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')

df = df.drop(columns=['chemical_class', 'chemical_sub_class', 'chemical_super_class', 
                      'np_classifier_pathway', 'np_classifier_superclass', 'np_classifier_class','organisms','ID'])

df = df.rename(columns={'identifier': 'coconut_id', 'canonical_smiles': 'smiles', 'standard_inchi': 'inchi', 'standard_inchi_key': 'inchi_key', 'name': 'compound_name', 'synonyms': 'synonyms', 'cas': 'cas'})

df = df.reset_index(drop=True)
df['compound_id'] = df.index + 1

new_order = ['compound_id', 'smiles', 'inchi', 'inchi_key','compound_name', 'synonyms', 'coconut_id', 'cas']
df = df[new_order]

df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv', index=False)"""

# getting the pubmed ids for the comounds

"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv')
cids = []

def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')
errors = []
counter = 0

for inchi_key in df['inchi_key']:
    time.sleep(0.5)
    counter += 1
    try:
        compounds = pcp.get_compounds(inchi_key, 'inchikey')
        if compounds:
            compound = compounds[0]
            cids.append(compound.cid)
            print(f"Compound: {compound.iupac_name}, PubMed IDs: {compound.cid}")
            progress_bar(counter, len(df['inchi_key']))
        else:
            print(f"No compound found for InChIKey: {inchi_key}")
            errors.append(inchi_key)
    except Exception as e:
        print(f"Error processing InChIKey {inchi_key}: {e}")
        errors.append(inchi_key)

df['cids'] = cids

df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv', index=False)
print(f"Errors for InChIKeys: {', '.join(errors)}")
"""
#getting the new plants into db ready format
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/unique_plants_with_correct_Names.csv')
refDF = pd.read_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/SANCDB_plants_for_DB.csv')

df['genus'] = df['original_name'].str.split(' ').str[0]
df['species'] = df['original_name'].str.split(' ').str[1]

df['gbif_key'] = df['gbif_accepted_id'].fillna(df['gbif_id'])
df['gbif_key'] = df['gbif_key'].astype(str).str.replace(r'\.0$', '', regex=True)

parts = df['original_name'].str.split(' ', n=2, expand=True)
dfEDGEcases = df.loc[parts[2].notna(), 'original_name']
print(dfEDGEcases)

df.to_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv', index=False)"""

#showing duplicates
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv')
duplicates = df[df.duplicated(subset=['gbif_key'], keep=False)]
print(duplicates)"""

# removing duplicates
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv')
df = df.drop_duplicates(subset=['gbif_key'], keep='first')
df.to_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv', index=False)"""

# getting all the entries where the species entry was empty to figure whats happeneing
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv')
empty_species = df[df['species'].isna()]

url = "https://api.gbif.org/v1/species/{}"


errors = []
for gbif_key, name in empty_species[['gbif_key', 'gbif_accepted_name']].values:

    try:
        time.sleep(0.1)
        r = requests.get(url.format(gbif_key), timeout=10)
        r.raise_for_status()
        data = r.json()
        family = data.get("family", "NA")
        genus_fromGBIF = data.get("genus", "NA")
        print(f"Processed: {gbif_key}")
        if isinstance(name, str) and name.strip():
            genus_local = name.strip().split()[0]   # "Euphorbia" from "Euphorbia esula"
        else:
            genus_local = None
        fam_norm = family.lower() if isinstance(family, str) else None
        gen_gbif_norm = genus_fromGBIF.lower() if isinstance(genus_fromGBIF, str) else None
        gen_local_norm = genus_local.lower() if genus_local else None
        if fam_norm and gen_local_norm and fam_norm == gen_local_norm:
            print(f'gbif says {name} is a family')
            df.drop(df[df['gbif_key'] == gbif_key].index, inplace=True)
        elif gen_gbif_norm and gen_local_norm and gen_gbif_norm == gen_local_norm:
            print(f'gbif says {name} is not a family')
            df.loc[df['gbif_key'] == gbif_key, 'species'] = 'spp.'
        else:
            print(f'this one is weird {name}')
            errors.append(f'this one is weird {name}')
    except requests.exceptions.RequestException as e:
        print(f"Error for {gbif_key}: {e}")
        errors.append(f"Error for {gbif_key}: {e}")

df.to_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv', index=False)
print(errors)
"""

#['this one is weird Launea Endl.', 'this one is weird Liliopsida', 'this one is weird Helianthopsis H.Rob.', 'this one is weird Myrsinaceae']
# now manually sorting these ones out
"""
df= pd.read_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv')

df.loc[df['gbif_accepted_name'] == 'Launea Endl.', 'species'] = 'spp.'
df.drop(df[df['gbif_accepted_name'] == 'Liliopsida'].index, inplace=True)
df.loc[df['gbif_accepted_name'] == 'Helianthopsis H.Rob.', 'species'] = 'spp.'
df.drop(df[df['gbif_accepted_name'] == 'Myrsinaceae'].index, inplace=True)

df.to_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv', index=False)"""

# using the gbif to query genus family and species for the plant db transfer

df = pd.read_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv')
errors = []

df['family'] = None

def progressbar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')

count = 0
url = "https://api.gbif.org/v1/species/{}"
for key in df['gbif_key']:
    time.sleep(0.4)
    count += 1
    try:
        r = requests.get(url.format(key), timeout=10)
        r.raise_for_status()
        data = r.json()
        family = data.get("family", "NA")
        genus = data.get("genus", "NA")
        species = data.get("species", "NA")
        df.loc[df['gbif_key'] == key, 'family'] = family
        df.loc[df['gbif_key'] == key, 'genus'] = genus
        df.loc[df['gbif_key'] == key, 'species'] = species
        print(f"Processed: {key}")
        progressbar(count, len(df['gbif_key']))
    except requests.exceptions.RequestException as e:
        print(f"Error for {key}: {e}")
        errors.append(f"Error for {key}: {e}")

df.to_csv('/home/school/masters/Scripts/ANPDB/plants_for_db.csv', index=False)
print(errors)

