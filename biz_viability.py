import pandas as pd
import re
from difflib import SequenceMatcher
import datetime
import pandasql as psql



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

    df = pd.read_csv(biz_data_path, nrows=50000000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[df['BUSINESS_ACTIVITY'].str.lower().str.contains('food', na = False)]
    df = df[['LICENSE_ID', 'DOING_BUSINESS_AS_NAME', 'ADDRESS', 'DATE_ISSUED', 'LICENSE_STATUS',
             'LICENSE_STATUS_CHANGE_DATE', 'ZIP_CODE']]
    df.ZIP_CODE = df.ZIP_CODE.astype(str)
    df = df[df.ZIP_CODE.str.match('6060[0-9]')]
    return df


def fetch_inspection_data():

    df = pd.read_csv(food_insp_data, nrows=500000000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['DBA_Name', 'Inspection_ID', 'License_#', 'Address', 'Inspection_Date', 'Results', 'Zip']]
    df = df.rename(columns={'License_#': 'LICENSE_ID', 'DBA_Name':'DOING_BUSINESS_AS_NAME','Address':'ADDRESS'})
    df.Zip = df.Zip.astype(str)
    df = df[df.Zip.str.match('6060[0-9]')]
    df = df[df['Results'].str.lower().str.contains('fail')]

    return df


def fetch_restaurant_data():
    df = pd.read_csv(rest_data_path, nrows=500000)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df[['name', 'address', 'categories']]
    df['address'] = df['address'].apply(lambda x: address_refine(x))
    df = df[df['categories'].str.lower().str.contains('restaurants')]
    return df


def integrate_inspection_business():
    pass


def normalise_biz_data():

    insp_data = fetch_inspection_data()
    biz_data = fetch_biz_data()
    regex = "[^ a-zA-Z0-9]"
    new_df = pd.DataFrame()

    for row in biz_data.index:

        x = biz_data.at[row, 'ADDRESS'].lower().split(" ")

        if len(x) > 3:

            tempFrame = insp_data[insp_data['ADDRESS'].str.lower().str.contains(x[0], na=False)]
            tempFrame = tempFrame[tempFrame['ADDRESS'].str.lower().str.contains(x[2], na=False)]
            name = biz_data.at[row, 'DOING_BUSINESS_AS_NAME'][:3]
            name = name.lower()
            tempFrame = tempFrame[tempFrame['DOING_BUSINESS_AS_NAME'].str.lower().str.startswith(name, na=False)]
            tempFrame = pd.DataFrame(
                {'total': tempFrame.groupby(["ADDRESS", "DOING_BUSINESS_AS_NAME"]).size()}).reset_index()

            org_name = re.sub(regex, "", biz_data.at[row, 'DOING_BUSINESS_AS_NAME'])

            for t_rows in tempFrame.index:
                temp_name = re.sub(regex, "", tempFrame.at[t_rows, 'DOING_BUSINESS_AS_NAME'])
                measure = similar(org_name, temp_name)
                if measure >= 0.7:
                    biz_data.at[row, "DOING_BUSINESS_AS_NAME"] = tempFrame.at[t_rows, 'DOING_BUSINESS_AS_NAME']
                    biz_data.at[row, "ADDRESS"] = tempFrame.at[t_rows, 'ADDRESS']
                    break
    biz_data.to_csv('normalised_biz_data.csv', encoding='utf-8', index=False)
    return biz_data


def normalise_inspection_data():

    insp_data = fetch_inspection_data()
    biz_data = fetch_biz_data()
    regex = "[^ a-zA-Z0-9]"
    new_df = pd.DataFrame()
    new_insp_data = pd.DataFrame(insp_data)
    insp_data = pd.DataFrame(
        {'total': insp_data.groupby(["ADDRESS", "DOING_BUSINESS_AS_NAME"]).size()}).reset_index()
    for row in insp_data.index:

        x = insp_data.at[row, 'ADDRESS'].lower().split(" ")

        if len(x) > 3:

            tempFrame = biz_data[biz_data['ADDRESS'].str.lower().str.contains(x[0], na=False)]
            tempFrame = tempFrame[tempFrame['ADDRESS'].str.lower().str.contains(x[2], na=False)]
            name = insp_data.at[row, 'DOING_BUSINESS_AS_NAME'][:3]
            name = name.lower()
            tempFrame = tempFrame[tempFrame['DOING_BUSINESS_AS_NAME'].str.lower().str.startswith(name, na=False)]
            tempFrame = pd.DataFrame(
                {'total': tempFrame.groupby(["ADDRESS", "DOING_BUSINESS_AS_NAME"]).size()}).reset_index()

            org_name = re.sub(regex, "", insp_data.at[row, 'DOING_BUSINESS_AS_NAME'])

            for t_rows in tempFrame.index:
                temp_name = re.sub(regex, "", tempFrame.at[t_rows, 'DOING_BUSINESS_AS_NAME'])
                measure = similar(org_name, temp_name)
                if measure >= 0.7:
                    new_insp_data.loc[(new_insp_data["DOING_BUSINESS_AS_NAME"] == org_name) &
                                      (new_insp_data["ADDRESS"] == insp_data.at[row, 'ADDRESS']), "DOING_BUSINESS_AS_NAME"] = tempFrame.at[t_rows, 'DOING_BUSINESS_AS_NAME']
                    new_insp_data.loc[(new_insp_data["DOING_BUSINESS_AS_NAME"] == org_name) &
                                      (new_insp_data["ADDRESS"] == insp_data.at[
                                          row, 'ADDRESS']), "ADDRESS"] = tempFrame.at[
                        t_rows, 'ADDRESS']
                    #new_insp_data.at[row, "ADDRESS"] = tempFrame.at[t_rows, 'ADDRESS']
                    break
    new_insp_data.to_csv('normalised_inspection_data.csv', encoding='utf-8', index=False)
    return new_insp_data



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
    return new_df[['LICENSE_ID','DOING_BUSINESS_AS_NAME', 'ADDRESS', 'DATE_ISSUED', 'LICENSE_STATUS', 'LICENSE_STATUS_CHANGE_DATE']]


def main():

    #yelp_integrated_frame = integrate_restaurants_business()
    yelp_integrated_frame = fetch_biz_data()
    inspection_data = fetch_inspection_data()
    inspection_data = inspection_data[inspection_data['Results'].str.lower().str.contains('fail')]
    yelp_integrated_frame['DATE_ISSUED'] = pd.to_datetime(yelp_integrated_frame['DATE_ISSUED'], format='%m/%d/%Y')
    yelp_integrated_frame['LICENSE_STATUS_CHANGE_DATE'] = pd.to_datetime(yelp_integrated_frame['LICENSE_STATUS_CHANGE_DATE'], format='%m/%d/%Y')
    inspection_data['Inspection_Date'] = pd.to_datetime(inspection_data['Inspection_Date'], format='%m/%d/%Y')


    inspection_data_test= inspection_data.groupby(['DOING_BUSINESS_AS_NAME', 'ADDRESS'])['Inspection_Date'].max().reset_index()

    yelp_int_test = yelp_integrated_frame.groupby(['DOING_BUSINESS_AS_NAME', 'ADDRESS'])['DATE_ISSUED'].max().reset_index()

    integ = pd.merge(inspection_data_test,yelp_int_test, on=['DOING_BUSINESS_AS_NAME'])

    #integ = integ.sort_values('DOING_BUSINESS_AS_NAME')

    #pysqldf = lambda q: sqldf(q, globals())

    new_df = pd.DataFrame()

    for dummy,index in integ.iterrows():
        add_x = index['ADDRESS_x']
        add_y = index['ADDRESS_y']
        measure = similar(add_x, add_y)
        if measure >= 0.8 and index['Inspection_Date'].year <= 2014:
            index["diff"] = (index['Inspection_Date'] - index['DATE_ISSUED']).days
            new_df = new_df.append(index)




    new_df = new_df[new_df['diff'] > 750]
    new_df = new_df[['DOING_BUSINESS_AS_NAME','ADDRESS_x','Inspection_Date', 'diff']]
    new_df = new_df.groupby(['DOING_BUSINESS_AS_NAME','ADDRESS_x'])['Inspection_Date','diff'].max().reset_index()



    q = """SELECT * FROM integ WHERE integ.ADDRESS_x LIKE '%' || integ.ADDRESS_y || '%'"""

    dff = psql.sqldf(q, locals())

    first_issued_lic_data = yelp_integrated_frame.groupby("DOING_BUSINESS_AS_NAME", as_index=False)["DATE_ISSUED"].max()
    yelp_integrated_frame = pd.merge(yelp_integrated_frame,first_issued_lic_data, on=['DOING_BUSINESS_AS_NAME','DOING_BUSINESS_AS_NAME',
                                                                                      'DATE_ISSUED','DATE_ISSUED',])
    yelp_integrated_frame = yelp_integrated_frame.drop_duplicates()

    yelp_integrated_frame = yelp_integrated_frame[yelp_integrated_frame['LICENSE_STATUS'].str.lower().str.contains('aac|rev')]

    merged = pd.merge(inspection_data,yelp_integrated_frame, on=['LICENSE_ID'])
    merged['diff'] = 0

    for dummy,index in merged.iterrows():
        merged.at[dummy,"diff"] = (index['LICENSE_STATUS_CHANGE_DATE'] - index['DATE_ISSUED']).days


    merged = merged[['DOING_BUSINESS_AS_NAME_x','ADDRESS_x','Inspection_Date','diff']]
    merged = merged.groupby(['DOING_BUSINESS_AS_NAME_x','ADDRESS_x'])['Inspection_Date','diff'].max().reset_index()

    merged = merged.rename(columns={'DOING_BUSINESS_AS_NAME_x': 'DOING_BUSINESS_AS_NAME'})


    final_merge = pd.concat([new_df, merged], ignore_index=True)
    final_merge = final_merge.groupby(['DOING_BUSINESS_AS_NAME','ADDRESS_x'])['Inspection_Date','diff'].max().reset_index()
    final_merge['diff'] = final_merge['diff'].apply(lambda x: float(x)/float(365))

    final_merge = final_merge.rename(columns={'DOING_BUSINESS_AS_NAME': 'Restaurant Name', 'Inspection_Date':'Failed inspection on','ADDRESS':'Address','diff':'Alive for x years'})
    final_merge.to_csv('biz_viability_out.csv', encoding='utf-8', index=False)







    print(yelp_integrated_frame)
    now = datetime.datetime.now()
    cur_year = now.year




main()
#normalise_inspection_data()
