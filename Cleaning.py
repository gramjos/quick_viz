#!/usr/bin/env python
import pandas as pd

df = pd.read_json('data.txt')

# attr names in first row so write them to column name
df.columns=df.iloc[0]
df=df.drop([0], axis=0) # drop that copied from label row

newCols=pd.Series([i.split(', ') for i in df["NAME"]])
states=pd.Series([s for c,s in newCols])
counties=pd.Series([c for c,s in newCols])

df_col = pd.DataFrame(data={'states':states,'county':counties})

# standardize indexes b/c .join() 
df=df.set_index(pd.Index([i for i in range(0,len(df))]))

df_join = df.join(df_col, lsuffix='_df_OG', rsuffix='_df_col')
cols={'NAME':'Name', 'B01001_001E':'Population', 'state':'state_no', 
    'county':'county_no', 'states':'State', 'county_df_col':'County',
    'county_df_OG':'County_no'}
fdf=df_join.rename(columns=cols)

fdf.to_csv('tidied_data.txt', index=False)