import csv

restaurant_data = {}
with open('reviews_60601-60606.csv', newline='') as rev:
    r = csv.reader(rev, delimiter=',')
    for row in r:
        if row[0] == 'date':
            continue
        rating = row[4].strip()
        num = 4
        while not rating.isdigit() and num <= len(row):
            rating = row[num-1].strip()
            num += 1
        try:
            rating = float(rating)
        except ValueError:
            print(rating)
        restaurant_id = row[-1].strip()
        try:
            restaurant_data[restaurant_id].append(rating)
        except KeyError:
            restaurant_data[restaurant_id] = []
            restaurant_data[restaurant_id].append(rating)
        # print("(" + str(i) + ")" + str(rating) + "  <----->  " + restaurant_id)

for key, val in restaurant_data.items():
    print(key, val)
