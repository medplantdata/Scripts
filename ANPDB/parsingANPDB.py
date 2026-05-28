from rdkit import Chem
from rdkit.Chem import PandasTools
import pandas as pd
import requests
import time

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
    