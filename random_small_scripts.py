"""columns = 'count,gbif_taxon_key,family,scientific_name,scientific_name_authorship,taxonomic_status,acceptednameusageid,parentnameusageid,originalnameusageid,namepublishedin,scientificnameid,dynamicproperties,references'
col = columns.split(',')
out = ''

for co in col:
    out = f'{out}, "{co.strip()}"'

print(out)"""

s1 = 'InChI=1S/C7H9N5O2/c1-12-3-4(10-7(12)13)9-6(8)11-5(3)14-2/h1-2H3,(H3,8,9,10,11,13)'
s2 = 'InChI=1S/C7H9N5O2/c1-12-3-4(10-7(12)13)9-6(8)11-5(3)14-2/h1-2H3,(H3,8,9,10,11,13)'

if s1 == s2:
    print('Equal')