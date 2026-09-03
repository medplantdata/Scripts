columns = 'count,gbif_taxon_key,family,scientific_name,scientific_name_authorship,taxonomic_status,acceptednameusageid,parentnameusageid,originalnameusageid,namepublishedin,scientificnameid,dynamicproperties,references'
col = columns.split(',')
out = ''

for co in col:
    out = f'{out}, "{co.strip()}"'

print(out)