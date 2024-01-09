import csv
import matplotlib.pyplot as plt
import math
import scipy

match_data = []
league_starts = {"E0": [], "E1": [], "E2": [], "E3": []}
league_ends = {"E0": [], "E1": [], "E2": [], "E3": []}
elo_params = [1500,64,400,1]

start_elos = {"E0": 4000, "E1": 3000, "E2": 2000, "E3": 1000}
leagues = ["Premiership","Championship","League 1","League 2"]
names = []

year_range = range(19,23)
year_num = len(year_range)
league_num = len(leagues)

for league in leagues:
    names.append([league + " 20" + str(x) + "-" + str(x+1) + ".csv" for x in year_range])

print(names)

for x in range(0,year_num):
    for y in range(0,league_num):
        name_data = []
        with open(names[y][x], 'r') as csv_data:
            open_data = []
            data_reader = csv.reader(csv_data)
            for data_row in data_reader:
                name_data.append(data_row)
        match_data += name_data[1:]


def elo_sigma(r,k,s):
    return (10 ** (r / s)) / ((10 ** ((-r) / s)) + k + (10 ** (r / s)))

def calc_elos_tester(data,params):
    teams = {}

    success = 0
    failure = 0
    attempts = 0
    success_tally = []

    profit = 0
    funds = 100
    stake = 10
    profit_tally = []
    winnings = 0
    win_odds = []

    odds_probs_tally = []
    elo_probs_tally = []

    start_elo = params[0]
    k_factor = params[1]
    scale_factor = params[2]
    k_draw = params[3]

    for row in data:
        h_team = row[2]
        a_team = row[3]
        winner = row[6]
        odds = [float(x) for x in row[26:29]]
        odd_probs = [1/x for x in odds]
        guess = ''

        elo_probs = [0, 0, 0]

        if h_team not in teams:
            teams[h_team] = start_elos[row[0]]
        if a_team not in teams:
            teams[a_team] = start_elos[row[0]]

        h_init_elo = teams[h_team]
        a_init_elo = teams[a_team]

        expected_score = 1 / (1 + (10 ** ((a_init_elo - h_init_elo) / scale_factor)))

        r = h_init_elo - a_init_elo

        elo_probs[0] = elo_sigma(r, k_draw, scale_factor)
        elo_probs[2] = elo_sigma(-r, k_draw, scale_factor)
        elo_probs[1] = k_draw * math.sqrt(elo_sigma(r, k_draw, scale_factor)*elo_sigma(-r, k_draw, scale_factor))

        actual_score = 0.5

        if winner == 'H':
            actual_score = 1
        elif winner == 'A':
            actual_score = 0
        else:
            actual_score = 0.5

        guess_odds = 0
        elo_odds = 0
        fav_is_guess = False

        if max(elo_probs) == elo_probs[0]:
            if max(odds) == odds[2]:
                fav_is_guess = True
            stake_diff = elo_probs[0]/odd_probs[0]
            guess = 'H'
            guess_odds = odds[0]
            odds_probs_tally.append(odd_probs[0])
            elo_probs_tally.append(elo_probs[0])
        elif max(elo_probs) == elo_probs[1]:
            if max(odds) == odds[2]:
                fav_is_guess = True
            stake_diff = elo_probs[1]/odd_probs[1]
            guess = 'D'
            guess_odds = odds[1]
            odds_probs_tally.append(odd_probs[1])
            elo_probs_tally.append(elo_probs[1])
        elif max(elo_probs) == elo_probs[2]:
            if max(odds) == odds[2]:
                fav_is_guess = True
            stake_diff = elo_probs[2]/odd_probs[2]
            guess = 'A'
            guess_odds = odds[2]
            odds_probs_tally.append(odd_probs[2])
            elo_probs_tally.append(elo_probs[2])

        print(guess_odds)
        stake = 10 * stake_diff

        profit = 0
        attempts += 1
        if winner == guess and winner == 'H':
            profit = (odds[0] * stake) - stake
            winnings += profit
            success += 1
            win_odds.append(odds[0])
        elif winner == guess and winner == 'D':
            profit = (odds[1] * stake) - stake
            winnings += profit
            success += 1
            win_odds.append(odds[1])
        elif winner == guess and winner == 'A':
            profit = (odds[2] * stake) - stake
            winnings += profit
            success += 1
            win_odds.append(odds[2])
        else:
            profit = -stake
            failure += 1
        success_tally.append([success, failure, attempts, success / attempts])

        print(profit)
        print(guess_odds)

        funds += min(profit,1000)

        print(funds)
        profit_tally.append(funds)

        h_adjusted_elo = max(100, h_init_elo + (k_factor * (actual_score - expected_score)))
        a_adjusted_elo = max(100, a_init_elo + (k_factor * -(actual_score - expected_score)))

        teams[h_team] = h_adjusted_elo
        teams[a_team] = a_adjusted_elo

    return teams, [success,failure,attempts,success_tally], [profit,funds,profit_tally,winnings,win_odds], [elo_probs_tally,odds_probs_tally]


def print_rankings(elo_dict):
    sorted_rankings = sorted(elo_dict.items(), key=lambda x:x[1])
    for x in sorted_rankings:
        print(x)


return_data = calc_elos_tester(match_data, elo_params)
success_list = [x[0] for x in return_data[1][3]]
failure_list = [x[1] for x in return_data[1][3]]
accuracy_list = [x[3] for x in return_data[1][3]]
funds_list = return_data[2][2]

print_rankings(return_data[0])

print()
test_prob = 0.514
p_test = scipy.stats.binom
print(p_test.cdf(return_data[1][0],return_data[1][2], test_prob))

print(sum(return_data[2][4])/len(return_data[2][4]))
print(return_data[2][1])
print(return_data[1][0]/return_data[1][2])

fig, ax = plt.subplots()
plt.title('Total P/L Over the 2019-2023 Seasons with Weighted Elo Bets')
plt.xlabel('Game Number')
plt.ylabel('Total P/L in GBP')
ax.plot(funds_list)
plt.savefig("Weighted Plot")
plt.show()
