import pandas as pd
df = pd.read_csv('Airbnb_Open_Data.csv', low_memory=False)
col_keep = ['id', 'NAME', 'host id', 'host_identity_verified', 'host name',
       'neighbourhood group', 'neighbourhood', 'lat', 'long', 'country',
       'country code', 'instant_bookable', 'cancellation_policy', 'room type',
       'Construction year', 'price', 'service fee']
col_delete = ['minimum nights',
       'number of reviews', 'last review', 'reviews per month',
       'review rate number', 'calculated host listings count',
       'availability 365', 'house_rules', 'license']
#to check missing values in each column
df.isna().sum()
df.drop(columns=col_delete, inplace=True) 
df.columns = (
    df.columns
      .str.strip()          # remove leading/trailing spaces
      .str.lower()          # lowercase
      .str.replace(' ', '_', regex=False)  # space → _
)
#to check duplicates
df.drop_duplicates(inplace=True)

#drop rows with missing values
df.dropna(inplace=True)

#data cleaning make datas uppercase
df['host_identity_verified'] = df['host_identity_verified'].str.upper()
df['instant_bookable']=df['instant_bookable'].apply(lambda x: 1 if x == 'TRUE' else 0 )    

#data cleaning price column replace $ and , then convert to int
df['price']=df['price'].str.replace(r'\$', '', regex=True).replace(r',', '', regex=True).astype(float)
df['price']=df['price'].astype(int)

df.reset_index(drop=True, inplace=True)    

df.to_csv('Airbnb_Cleaned_Data.csv', index=False)
df.to_excel('Airbnb_Cleaned_Data.xlsx', index=False)    



