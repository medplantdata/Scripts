import pandas as pd
import sys
# extracts coconut_id and organism 
plant_file = '/home/school/masters/Scripts/wcvp_dwca/wcvp_taxon.csv'
input_file_path = '/home/school/masters/Scripts/coconut_full/coconut_full.csv'
error_path = ''
output_path = ''



df = pd.read_csv(input_file_path)
entries = []

for idx, row in df.iterrows():
    coconut_id = row['identifier']
    orgs = row['organisms']
    if pd.isna(orgs) == False:
        organisms = orgs.split('|')
        clean_organisms = [organism.strip() for organism in organisms]
        for organism in clean_organisms:
            entries.append([coconut_id,organism])

coconut_organisms= pd.DataFrame(entries, columns=['coconut_id','scientificName'])
print('finished plant sep')
coconut_organisms.to_csv('/home/school/masters/Scripts/coconut_full/coconut_organisms.csv')

"""
seperated_plants_df = pd.DataFrame(entries,columns=['coconut_id','plant_name_from_coconut'])
plant_df = pd.read_csv(plant_file, sep= '|')

entries = []
entry = []
errors = []

for idx, row in seperated_plants_df.iterrows():
    full_name = row['plant_name_from_coconut']
    full_name = full_name.strip()
    genus = full_name.split()[0]
    species = full_name.split()[1]
    coconut_id = seperated_plants_df['coconut_id']


    if plant_df['scientfiicname'].str.lower().isin([full_name.lower()]):
        plant_row = plant_df.loc(plant_df['scientfiicname'] == full_name)
        if plant_row['taxonomicstatus'] == 'accepted':
            for idx, row in plant_row.iterrows():
                entry = [coconut_id,full_name,row['taxonid']]
        elif pd.isna(plant_row['acceptedusagenameid']):
            errors = [coconut_id, full_name, 'the name was not relateable to a proper ID via the WCVP']
        else:
            accepted_id = plant_row['acceptedusagenameid']
            accepted_row = plant_df.loc[plant_df['taxonid'] == accepted_id]
            entry = [coconut_id,full_name,accepted_row['taxonid']] 
    else:
        print(full_name)
        errors = [coconut_id, full_name, 'WCVP does not have a synonym for this one']
        sys.exit()

df_with_accepted_names = pd.DataFrame(entries, columns = ['coconut_id', 'coconut_name', 'accepted_id'])
"""
