import pandas as pd
import csv

review_file=open("reviews_60601-60606.csv","r")
clean_reviwes_file=open("clean_reviews_60601-60606.csv","w")
review_reader=csv.reader(review_file)
review_writer=csv.writer(clean_reviwes_file)
count=0
total_count=0
for line in review_reader:
    if len(line)>10:
        str=''
        str=line[3]
        initial=4
        while(initial<len(line)-6):
            str=str+(line[initial])
            del line[initial]        
        line[3]=str
        count=count+1
    review_writer.writerow(line)
    total_count=total_count+1

reviews_pd=pd.read_csv("clean_reviews_60601-60606.csv")
final_pd=reviews_pd[['reviewContent','rating']]
final_pd.to_csv("preprocessed_reviews_file.csv")
clean_reviwes_file.close()
print("Given reviews file has reviews split into different columns - now they are combined and the reviews file is made into a singular format - and required information fro next steps is gathered and stored in a single file")