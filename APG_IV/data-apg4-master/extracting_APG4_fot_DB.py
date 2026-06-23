import pandas as pd

#////////////////////////////////////////////////this bit extracts the orders and gives them an id, then saves to a csv file.//////////////////////////////////////////////////////
"""apgDF = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/apg4_data.csv')
apgDF.columns = apgDF.columns.str.strip()  
print(apgDF.columns.to_list())


ordersDF = pd.DataFrame(columns=['order_id', 'order'])
orders = []
order_count = 0

for name, taxonRank in apgDF[['Scientific Name','Taxon Rank']].values:
    if taxonRank == 'order':
        order_count += 1
        orders.append([order_count, name])

ordersDF = pd.DataFrame(orders, columns=['order_id', 'order'])
ordersDF.to_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/orders.csv', index=False)
"""
#////////////////////////////////////////////////this bit extracts the families and gives them an id, and a FK to the order then saves to a csv file
"""apgDF = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/apg4_data.csv')
apgDF.columns = apgDF.columns.str.strip()

ordersDF = pd.DataFrame(columns=['order_id', 'order'])
familiesDF = pd.DataFrame(columns=['family_id', 'family', 'order_id'])
orders = []
families = []
order_count = 0
family_count = 0

for name, taxonRank in apgDF[['Scientific Name','Taxon Rank']].values:
    if taxonRank == 'order':
        order_count += 1
        orders.append([order_count, name])
    elif taxonRank == 'family':
        family_count += 1
        families.append([family_count, name, order_count])

familiesDF = pd.DataFrame(families, columns=['family_id', 'family', 'order_id'])
familiesDF.to_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/families.csv', index=False)
"""

# generating list of all the families

df = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/families.csv')
families = df['family'].tolist()
print(families)
