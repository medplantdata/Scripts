import requests
import time
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

extracted_neurologicalsDF = pd.read_csv("/home/school/masters/Scripts/ExtractedNeurologicals.csv")

def get_smiles_from_pubchem(compound_name):
    time.sleep(6)  
    cleaned_name = " ".join(compound_name.split())
    encoded_name = requests.utils.quote(cleaned_name)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/property/CanonicalSMILES/TXT"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"Fetched SMILES for {compound_name}: {response.text.strip()}") 
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching SMILES for {compound_name}: {e}")
        return 'Sum dodgy here'

extracted_neurologicalsDF['SMILES'] = extracted_neurologicalsDF['Drug name'].apply(get_smiles_from_pubchem)
extracted_neurologicalsDF.to_csv("ExtractedNeurologicalsWithSMILESFromZhu2011.csv", index=False)