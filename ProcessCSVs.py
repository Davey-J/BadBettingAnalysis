import csv

data = []

names = ["Premiership 20" + str(x) + "-" + str(x+1) for x in range(12,19)]

for file in names:
    name_data = []
    with open(file  + ".csv", 'r') as csv_data:
        data_reader = csv.reader(csv_data)
        for data_row in data_reader:
            name_data.append(data_row)
        print(name_data[0])
        if name_data[0][24] == "AvgH":
            for i in range(0,len(name_data)):
                name_data[i] = name_data[i][:24] + name_data[i][25:28:2] + name_data[i][24:29:2] + name_data[i][29:32:2] +name_data[i][30:33:2]

    with open(file + "Processed.csv", 'w', newline='') as csv_data:
        data_writer = csv.writer(csv_data)
        for row in name_data:
            data_writer.writerow(row)