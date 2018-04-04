from utils import jaccard, address_refine

import csv

restaurant_data = {}
# with open('reviews_60601-60606.csv', newline='') as rev:
#     r = csv.reader(rev, delimiter=',')
#     for row in r:
#         if row[0] == 'date':
#             continue
#         rating = row[4].strip()
#         num = 4
#         while not rating.isdigit() and num <= len(row):
#             rating = row[num-1].strip()
#             num += 1
#         try:
#             rating = float(rating)
#         except ValueError:
#             print(rating)
#         restaurant_id = row[-1].strip()
#         try:
#             restaurant_data[restaurant_id].append(rating)
#         except KeyError:
#             restaurant_data[restaurant_id] = []
#             restaurant_data[restaurant_id].append(rating)
#         # print("(" + str(i) + ")" + str(rating) + "  <----->  " + restaurant_id)

# for key, val in restaurant_data.items():
#     sum = 0
#     for x in val:
#         sum += x
#     avg = sum/len(val)
#     restaurant_data[key] = []
#     restaurant_data[key].append(avg)

with open('restaurants_60601-60606.csv', newline='', encoding='utf8') as rev:
    r = csv.reader(rev, delimiter=',')
    for row in r:
        if row[1] == 'name':
            continue
        id = row[0].strip()
        name = row[1].strip()
        address = row[6].strip()
        rating = float(row[4].strip())
        try:
            restaurant_data[id].append(name)
            restaurant_data[id].append(address)
            restaurant_data[id].append(rating)

        except KeyError:
            restaurant_data[id] = []
            restaurant_data[id].append(name)
            restaurant_data[id].append(address)
            restaurant_data[id].append(rating)


# for key, val in restaurant_data.items():
#     print(key, val)

with open('Food_Inspections.csv', newline='', encoding='utf8') as rev:
    r = csv.reader(rev, delimiter=',')
    i = 0
    for key, val in restaurant_data.items():
        i += 1
        name1 = val[0]
        address1 = address_refine(val[1])
        # if i > 30:
        #     break
        if address1 == "":
            continue
        flag = 0
        pass_inspection = 0
        fail_inspection = 0
        conditional_inspection = 0
        rev.seek(0)
        for row in r:
            name2 = row[1].strip()
            address2 = row[5].strip()

            if (jaccard(address1, address2) >= 0.9 and jaccard(name1, name2) >= 0.4) or (jaccard(address1, address2) >= 0.5 and jaccard(name1, name2) >= 0.5):
                print(name1, name2, address1, address2)
                result = row[9].strip().lower()
                if "pass" in result and "conditions" in result:
                    conditional_inspection += 1
                elif "pass" in result:
                    pass_inspection += 1
                elif "fail" in result:
                    fail_inspection += 1

        restaurant_data[key].append(pass_inspection)
        restaurant_data[key].append(conditional_inspection)
        restaurant_data[key].append(fail_inspection)

with open('query_4.csv', 'w', newline='', encoding='utf8') as writeFile:
    writer = csv.writer(writeFile, delimiter=',')
    writer.writerow(["Restaurant Name", "Address", "Average Yelp Review", "#Pass", "#Conditional", "#Failed Inspection"])
    for key, val in restaurant_data.items():
        try:
            if val[3] == 0 and val[4] == 0 and val[5] == 0:
                continue
        except IndexError:
            continue
        writer.writerow(val)
