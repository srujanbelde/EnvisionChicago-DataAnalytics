import pandas as pd
import pandasql as ps
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
import sklearn.metrics


data_path = "data/envision_chicago_reference_alignment.csv"
data_path1 = "data/Crimes.csv"


def decision_tree_model():

    data = pd.read_csv(data_path)


    crime_data = pd.read_csv(data_path1, nrows=50000000)
    crime_data = crime_data[["Case Number","Primary Type", "Community Area"]]
    crime_data = crime_data.rename(columns={'Case Number': 'Case'})
    merged = pd.merge(data, crime_data, on=['Case','Case'])
    merged['Address'] = merged['Address'].apply(lambda x: sum(ord(ch) for ch in str(x)))
    merged = merged.dropna()
    predictors = merged[['Address', 'Community Area']]

    target = merged[['Primary Type']]
    pred_train, pred_tests, tar_train, tar_test = train_test_split(predictors, target, test_size=.4)
    clf = DecisionTreeClassifier()
    clf.fit(pred_train, tar_train)
    pred = clf.predict_proba(pred_tests)
    print(pred)
    print("done!!")


decision_tree_model()