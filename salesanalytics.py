import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
files = [
    'Sales_January_2019.csv',
    'Sales_February_2019.csv',
    'Sales_March_2019.csv',
    'Sales_April_2019.csv',
    'Sales_June_2019.csv',
    'Sales_May_2019.csv',
    'Sales_July_2019.csv',
    'Sales_August_2019.csv',
    'Sales_September_2019.csv', 
    'Sales_October_2019.csv',
    'Sales_November_2019.csv',
    'Sales_December_2019.csv'
]
folder = Path('Sales_Data')
files = folder.glob('*.csv')
dfs = [pd.read_csv(f) for f in files]
df= pd.DataFrame()
df = pd.concat(dfs)
df.columns = (
    df.columns
      .str.strip()          # remove leading/trailing spaces
      .str.lower()          # lowercase
      .str.replace(' ', '_', regex=False)  # space → _
)

#change order_date to date time format
df['order_date'] = pd.to_datetime(
    df['order_date'],
    format='%m/%d/%y %H:%M',
    errors='coerce'
)
#assign new column 'month' from order_date
df['month'] = df['order_date'].dt.month

#drop all nan values
df.dropna(inplace=True)
df['month'] = df['month'].astype('int32')
df['sales'] = df['quantity_ordered'].astype(float) * df['price_each'].astype(float)
df['city'] = df['purchase_address'].apply(lambda x: x.split(',')[1].strip())
df['grouped'] = df.groupby('order_id')['product'].transform(lambda x: ','.join(x))

# #visualize sales by city
top_sales_city = df.groupby('city')['sales'].sum()
range_vals = df['city'].unique()
plt.bar(range_vals, top_sales_city)
plt.show()

#visualize total sales per month
top_sales_mn = df.groupby('month')['sales'].sum()
range_vals = range(1, 13)
plt.bar(range_vals, top_sales_mn)
plt.show()

#what is the pick hour for sales
df['hour'] = df['order_date'].dt.hour
top_sales_hr = df.groupby('hour')['sales'].sum()
range_vals = range(0, 24)
plt.plot(range_vals, top_sales_hr)
plt.xticks(range_vals)   # 👈 force all hours to show
plt.xlabel('Hour of Day')
plt.ylabel('Sales')
plt.title('Sales by Hour')
plt.grid()
plt.show()

# #export and import for testing
df.to_csv('Sales_2019_Combined.xlsx', index=False)
df2 = pd.read_csv('Sales_2019_Combined.xlsx')

