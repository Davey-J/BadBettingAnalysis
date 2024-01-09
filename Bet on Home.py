import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

data = []
bet_on_fav = []

names = ["Premiership 20" + str(x) + "-" + str(x+1) + ".csv" for x in range(19,23)]

for file in names:
    name_data = []
    with open(file, 'r') as csv_data:
        open_data = []
        data_reader = csv.reader(csv_data)
        for data_row in data_reader:
            name_data.append(data_row)
    data += name_data[1:]

for game in data[1:]:
    odds = game[26:29]
    profit = 0
    winner = game[6]

    if 'H' == winner:
        profit = (10*float(odds[0]))-10
    else:
        profit = -10

    bet_on_fav.append([winner, float(odds[0]), profit])

total_wins = 0
running_tally = []

for x in bet_on_fav:
    print(x)
    if x[2] < 0:
        total_wins += x[2]
    else:
        total_wins += x[2]-10
    running_tally.append(total_wins)

print(total_wins)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(range(0,len(running_tally)), running_tally)  # Plot some data on the axes.
plt.show()