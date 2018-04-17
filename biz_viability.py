import pandas as pd
import re
from difflib import SequenceMatcher


biz_data_path = "data/Business_Licenses.csv"
rest_data_path = "data/restaurants_60601-60606.csv"
food_insp_data = "data/Food_Inspections.csv"
out_data_path = "biz_viability.csv"


"""
Utility Functions
"""


def similar(a, b):
    a = a.lower()
    b = b.lower()
    regex = "[^ a-zA-Z0-9]"
    a = re.sub(regex, "", a)
    b = re.sub(regex, "", b)
    return SequenceMatcher(None, a, b).ratio()


def address_refine(str1):
    ad = str1.split()
    s = ""
    try:
        for x in ["st", "dr", "ave", "pl", "pky", "blvd"]:
            if x in ad[2].lower().strip():
                for n in range(0, 3):
                    s += ad[n] + " "
            elif x in ad[3].lower().strip():
                for n in range(0, 4):
                    s += ad[n] + " "
    except IndexError:
        return str1

    return replacing(s)


def replacing(a):
    a = a.lower()
    a = a.replace('avenue', 'ave')
    a = a.replace('street', 'st')
    a = a.replace('boulevard', 'blvd')
    a = a.replace('parkway', 'pky')
    a = a.replace('place', 'pl')
    a = a.replace('drive', 'dr')
    a = a.replace('\'', '')
    a = a.replace('and', '&')
    a = a.replace('express', 'exp')
    a = a.replace('pizzeria', 'pizza')
    a = a.replace('academy', 'ady')
    a = a.replace('union station', 'usn')
    a = a.replace('cafe', 'cf')
    a = a.replace('  ', ' ')
    return a


"""
Main Functions
"""


def fetch_biz_data():

    df = pd.read_csv(biz_data_path, nrows=5000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['LICENSE_ID', 'DOING_BUSINESS_AS_NAME', 'ADDRESS', 'DATE_ISSUED', 'LICENSE_STATUS', 'LICENSE_STATUS_CHANGE_DATE', 'ZIP_CODE']]
    df.ZIP_CODE = df.ZIP_CODE.astype(str)
    df = df[df.ZIP_CODE.str.match('6060[0-9]')]
    return df


def fetch_inspection_data():

    df = pd.read_csv(food_insp_data, nrows=5000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['DBA_Name', 'Inspection_ID', 'License_#', 'Address', 'Inspection_Date', 'Results', 'Zip']]
    df['License_#'] = ['License_Id']
    df.ZIP_CODE = df.ZIP_CODE.astype(str)
    df = df[df.ZIP_CODE.str.match('6060[0-9]')]
    return df


def fetch_restaurant_data():
    df = pd.read_csv(rest_data_path, nrows=5000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['name', 'address', 'categories']]
    df['address'] = df['address'].apply(lambda x: address_refine(x))
    df = df[df['categories'].str.lower().str.contains('restaurants')]
    return df


def integrate_restaurants_business():

    rest_data = fetch_restaurant_data()
    biz_data = fetch_biz_data()
    rest_data['DOING_BUSINESS_AS_NAME'] = ""
    rest_data['ADDRESS'] = ""
    regex = "[^ a-zA-Z0-9]"
    new_df = pd.DataFrame()

    for row in rest_data.index:

        x = rest_data.at[row,'address'].lower().split(" ")

        if len(x) > 3:

            tempFrame = biz_data[biz_data['ADDRESS'].str.lower().str.contains(x[0], na =False)]
            tempFrame = tempFrame[tempFrame['ADDRESS'].str.lower().str.contains(x[2], na =False)]
            name = rest_data.at[row, 'name'][:3]
            name = name.lower()
            tempFrame = tempFrame[tempFrame['DOING_BUSINESS_AS_NAME'].str.lower().str.startswith(name, na =False)]
            tempFrame = pd.DataFrame({'total': tempFrame.groupby(["ADDRESS","DOING_BUSINESS_AS_NAME"]).size()}).reset_index()

            for t_rows in tempFrame.index:
                org_name = re.sub(regex,"",rest_data.at[row,'name'])
                temp_name = re.sub(regex,"",tempFrame.at[t_rows,'DOING_BUSINESS_AS_NAME'])
                measure = similar(org_name, temp_name)
                if measure >= 0.7:
                    rest_data.at[row,"DOING_BUSINESS_AS_NAME"] = tempFrame.at[t_rows,'DOING_BUSINESS_AS_NAME']
                    rest_data.at[row, "ADDRESS"] = tempFrame.at[t_rows,'ADDRESS']
                    """
                    rest_data.at[row, "LICENSE_ID"] = tempFrame.at[t_rows, 'LICENSE_ID']
                    rest_data.at[row, "DATE_ISSUED"] = tempFrame.at[t_rows, 'DATE_ISSUED']
                    rest_data.at[row, "LICENSE_STATUS"] = tempFrame.at[t_rows, 'LICENSE_STATUS']
                    rest_data.at[row, "LICENSE_STATUS_CHANGE_DATE"] = tempFrame.at[t_rows, 'LICENSE_STATUS_CHANGE_DATE']
                    rest_data.at[row, "LICENSE_ID"] = tempFrame.at[t_rows, 'LICENSE_ID']
                    """
                    new_df = new_df.append(rest_data.loc[[row]])
                    break
    new_df = pd.merge(biz_data,new_df, on=['DOING_BUSINESS_AS_NAME','DOING_BUSINESS_AS_NAME','ADDRESS', 'ADDRESS'])
    print(new_df)

    #return new_df[['LICENSE_ID', 'DOING_BUSINESS_AS_NAME', 'ADDRESS', 'DATE_ISSUED', 'LICENSE_STATUS', 'LICENSE_STATUS_CHANGE_DATE']]


def main():
    yelp_integrated_frame = integrate_restaurants_business()
    print(yelp_integrated_frame)


main()
