import pandas as pd
import numpy as np

file_name = 'for_crime_classification.csv'
useless_cols = ['Name', 'DBA Name',
                'LICENSE DESCRIPTION', 'Risk',
                'Case #', 'DateTime', 'MaxTemp',
                'Census Block', 'Tract ID', 'Geo ID']
manual_df = pd.read_csv("Manaual Reference Alignment Envision Chicago.csv")
manual_df = manual_df[manual_df.DataSource != 'Business Licenses']
manual_df = manual_df[manual_df.DataSource != 'Food Inspection']
manual_df = manual_df[manual_df.DataSource != 'Weather']
manual_df = manual_df[manual_df.DataSource != 'Yelp']
manual_df = manual_df[manual_df.DataSource != 'Census']
manual_df = manual_df.drop(useless_cols, axis=1)
# manual_df = np.where(manual_df['Group ID'] == 0)
demographics_df = manual_df[manual_df['DataSource'] == 'DemoGraphics']
dict = {}
for index, row in demographics_df.iterrows():
    male = (row['Total Males']/row['Total Population'])*100
    female = (row['Total Female']/row['Total Population'])*100
    key = row['Group ID']
    dict[key] = []
    dict[key].append(male)
    dict[key].append(female)
    dict[key].append(row['Median Age'])
print(dict)
for key, value in dict.items():
    manual_df['Total Males'] = np.where((manual_df['Group ID'] == key) & (manual_df['DataSource'] == 'Crime'), value[0], manual_df['Total Males'])
    manual_df['Total Female'] = np.where((manual_df['Group ID'] == key) & (manual_df['DataSource'] == 'Crime'), value[1], manual_df['Total Female'])
    manual_df['Median Age'] = np.where((manual_df['Group ID'] == key) & (manual_df['DataSource'] == 'Crime'), value[2], manual_df['Median Age'])

manual_df = manual_df[manual_df.DataSource != 'DemoGraphics']
manual_df = manual_df.drop('Total Population', axis=1)

cols = manual_df.columns.values
cols[4] = 'Crime Type'
cols[5] = 'Male%'
cols[6] = 'Female%'
manual_df.colums = cols

manual_df.to_csv(file_name)
