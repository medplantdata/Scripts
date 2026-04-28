import pandas as pd

apgDF = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/apg4_data.csv')
apgDF.columns = apgDF.columns.str.strip()  
print(apgDF.columns.to_list())


ordersDF = pd.DataFrame(columns=['id', 'order'])
orders = []
count = 0

for name, taxonRank in apgDF[['Scientific Name','Taxon Rank']].values:
    if taxonRank == 'order':
        count += 1
        orders.append([count, name])

ordersDF = pd.DataFrame(orders, columns=['id', 'order'])
ordersDF.to_csv('orders.csv', index=False)

