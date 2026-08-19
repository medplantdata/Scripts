import pandas as pd
import sys
# extracts coconut_id and organism 
plant_file = '/home/school/masters/Scripts/wcvp_dwca/wcvp_taxon.csv'
input_file_path = '/home/school/masters/Scripts/coconut_full/coconut_full.csv'
error_path = ''
output_path = ''

# getting the coconut_id and organism from the coconut_full.csv file to send to the checkilist thingy
"""
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
coconut_organisms.to_csv('/home/school/masters/Scripts/coconut_full/coconut_organisms.csv', index=False)
"""


# code below was supposed to check the names against the WCVP but but I decided to do this differently
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


# pulling non plantae from coconut plants and deduplicating on the origional name from coconut_full.csv
"""
df = pd.read_csv('/home/school/masters/Scripts/coconut_full/checklist_matched_organisms.tsv',sep='\t')

entries = []
for row in df.itertuples(index=False):
    if row.kingdom == 'Plantae':
        entries.append(row)

old_len = len(df)
formatted = f"{old_len:,}".replace(",", " ")
print(f"The file sent had 1 267 087 entires and the one that came back has {old_len} (there are lots of dups still 
      in theory not just because of plant synonyms but because the same plants are repeated)")

df_plants = pd.DataFrame(entries, 
                         columns=['original_coconut_id','original_scientificName','matchType','matchIssues','ID','rank',
                                  'scientificName','authorship','status','acceptedID','acceptedScientificName',
                                  'acceptedAuthorship','kingdom','phylum','class','order','family','genus','classification'])

new_len = len(df_plants)
formatted = f"{new_len:,}".replace(",", " ")
print(f'The plants only (not deduplicated) is {formatted}')

df_plants.drop_duplicates('original_scientificName',inplace=True)

new_len = len(df_plants)
formatted = f"{new_len:,}".replace(",", " ")
print(f'The plants now with origional name deduplications removed is {formatted}')

df_plants.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants_still_needs_synonym_deduplication.csv', index=False)
"""

"""
# seeing what the options are for some of the ranks to fin what to excclude

df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/coconut_plants_still_needs_synonym_deduplication.csv')

match_types = df['matchType'].unique()
match_issues = df['matchIssues'].unique()

print(f'Types of matches are: {match_types}')
print(f'Types of match issues are: {match_issues}')
"""


# making a script that seperates the plants that worked so I can deduplicate on synonyms and assign accepted names
"""
df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/coconut_plants_still_needs_synonym_deduplication.csv')

df.drop(columns=['original_coconut_id'],inplace=True)

entries = []
naughty_names = []

for row in df.itertuples(index=False):
    if (row.matchType not in ['ambiguous','higherrank']) and pd.isna(row.matchIssues):
        entries.append(row)
    else:
        naughty_names.append(row)

column_names = df.columns

worked_df = pd.DataFrame(entries, columns=column_names)
worked_df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/to_be_deduplicated_validated_plants.csv',index=False)

no_df = pd.DataFrame(naughty_names,columns=column_names)
no_df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/checklist_error_plants.csv',index=False)
"""

