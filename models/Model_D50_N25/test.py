import joblib
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

loaded_rf = joblib.load("whole_dataset.joblib")
with open ('model_cols', 'rb') as fp:
    needed_cols = pickle.load(fp)

query_dict = {'BOROUGH':[2],'BUILDING CLASS CATEGORY':['01 ONE FAMILY HOMES'],'ZIP CODE':[10457],'RESIDENTIAL_UNITS':[1],'COMMERCIAL UNITS':[0],'TOTAL UNITS':[1],'LAND_SQUARE_FEET':[1768],'GROSS_SQUARE_FEET':[1188],'YEAR BUILT':[1901],'TAX CLASS AT TIME OF SALE':[1],'BUILDING CLASS AT TIME OF SALE':['A5'],'SALE DATE':['2009-3-15 00:00:00']}



with open ('model_cols', 'rb') as fp:
    needed_cols = pickle.load(fp)


max_date = pd.to_datetime('2019-12-31 00:00:00')
query_df = pd.DataFrame.from_dict(query_dict)
query_df = query_df.astype({'RESIDENTIAL_UNITS':'int64'})
query_df = query_df.astype({'COMMERCIAL UNITS':'int64'})
query_df = query_df.astype({'TOTAL UNITS':'int64'})
query_df = query_df.astype({'LAND_SQUARE_FEET':'int64'})
query_df = query_df.astype({'GROSS_SQUARE_FEET':'int64'})
query_df = query_df.astype({'YEAR BUILT':'int64'})
query_df['Date'] = 0

query_df['SALE DATE'] = pd.to_datetime(query_df['SALE DATE'])

def month_distance(start, end):
    mdiff = (end.year - start.year) * 12 + end.month - start.month
    return mdiff

for i, row in query_df.iterrows():
    query_df.at[i,'Date'] = month_distance(row['SALE DATE'],max_date)
query_df.set_index('SALE DATE', inplace=True)
query_df = pd.get_dummies(query_df, columns = ['Date'], prefix = 'Date')

# one_hots = ['BOROUGH','NEIGHBORHOOD','BUILDING CLASS CATEGORY','ZIP CODE','TAX CLASS AT TIME OF SALE','BUILDING CLASS AT TIME OF SALE']
one_hots = ['BOROUGH','BUILDING CLASS CATEGORY','ZIP CODE','TAX CLASS AT TIME OF SALE','BUILDING CLASS AT TIME OF SALE']
query_df = pd.get_dummies(query_df, columns = one_hots, prefix = one_hots)
# query_df.set_index('SALE DATE', inplace=True)
# date_range_sample = ['2003-01-01' , '2007-12-31']
# date_range_target = ['2008-01-01' , '2008-01-31']



for col in needed_cols:
    if col not in query_df.columns:
        query_df[col]=0

query_df = query_df.reindex(columns=needed_cols)


predicted_val = loaded_rf.predict(query_df.drop(columns =['SALE_PRICE']))
print(predicted_val[0])
