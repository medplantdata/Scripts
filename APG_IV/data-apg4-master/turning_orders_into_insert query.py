import pandas as pd

df = pd.read_csv('/home/school/masters/Scripts/APG_IV/data-apg4-master/orders.csv')

out = 'INSERT INTO orders (order_id, order_name) VALUES\n'

for id, order in df.itertuples(index=False):
    out += f"({id}, '{order}'),\n"

out = out[:-2] + ';'
print(out)
