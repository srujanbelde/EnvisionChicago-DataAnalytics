import pandas as pd
import re
from difflib import SequenceMatcher
import datetime

crimes_file_path = "Crimes_Census_Final_output.csv"
census_ages = "age_groups.csv"


def integrate_ages_crimes():
    crimes_census = pd.read_csv(crimes_file_path, nrows=50000000)
    crimes_census.columns = [c.replace(' ', '_') for c in crimes_census.columns]
    crimes_census['tract_block'] = crimes_census['tract_block'].apply(lambda x: fun(x))
    crimes_census = crimes_census.rename(columns={"tract_block": "census_block"})

    census_demographs = pd.read_csv(census_ages, nrows=50000000)
    census_demographs.columns = [c.replace(' ', '_') for c in census_demographs.columns]
    census_demographs['census_block'] = census_demographs.apply(lambda row: my_fun(row), axis=1)
    census_demographs['max_age'] = census_demographs.apply(lambda row: my_fun2(row), axis=1)


    integrated = pd.merge(census_demographs,crimes_census, on=['census_block'])

    return integrated
    print("hello")


def my_fun2(row):
    dict = {
        "5-17": row['Pop_5_17'],
        "18-24": row['Pop_18_24'],
        "25-44": row['Pop_25_44'],
        "45-64": row['Pop_45_64'],
        "65+": row['Pop_65']
    }
    age_grp = max(dict, key=dict.get)
    return age_grp


def my_fun(row):
    return int(str(row['tract']) + str(row['block_group']))


def fun(x):
    st = str(x)
    st = st[:-3]
    x = int(st)
    return x


def main():
    df = integrate_ages_crimes()

    no_crimes_data = pd.DataFrame({'crimes_no': df.groupby(['census_block','Primary_Type','year']).size()}).reset_index()
    df = pd.DataFrame({'unique': df.groupby(['census_block','max_age']).size()}).reset_index()
    df = df[['census_block', 'max_age']]
    final_frame = pd.merge(df,no_crimes_data,on=['census_block'])
    final_frame.to_csv('crime_statistics_out.csv', encoding='utf-8', index=False)



    print("done")




main()