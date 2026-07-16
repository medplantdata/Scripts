import pandas as pd

og_df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')
compound_df = pd.read_csv('/home/school/masters/Scripts/ANPDB/compound_stuff/anpdb_compounds_for_dbclean.csv')
plant_df = pd.read_csv('/home/school/masters/Scripts/ANPDB/plants_to_send_to_db.csv')


plants = {}
for plant_id, genus, species, synonyms in plant_df[['plant_id','genus','species','synonyms']].values:
    if pd.isna(synonyms):
        name = f"{genus} {species}"
    else:
        name = synonyms
    name.strip()
    plants[name] = plant_id

plant_id = ''
entries = []


count = 0
for identifier, organisms in og_df[['identifier','organisms']].values:
    compound_id = compound_df.loc[compound_df['coconut_id'] == identifier, 'compound_id'].iat[0]
    compound_id = int(compound_id)
    for organism in organisms.split('|'):
        if organism.strip() in plants:
            plant_id = plants[organism]
            entries.append([compound_id, plant_id])
        else:
            count += 1

df_out = pd.DataFrame(entries, columns=['compound_id', 'plant_id'])
df_out.to_csv('/home/school/masters/Scripts/ANPDB/compound_plant_relationships.csv', index=False)

print(count)