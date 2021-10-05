# this program will not finish unless you give it an abundance of time
# on a monster of a machine. Even then I really don't know. Never seen
# it finish personally

import pandas as pd

CURRENT_WEEK = 5    # change this depending on what week you're starting from
MIN_SCORE = 10000

def solve(used, score, week, grid, final_teams):
    global MIN_SCORE, CURRENT_WEEK

    # base case
    if week == 19:
        if score < MIN_SCORE:
            MIN_SCORE = score
            final_teams.clear()
            for team in used:
                final_teams.append(team)
        return

    # go through grid to look at spreads for the week
    for row in grid:

        # make sure we're not using a team twice
        if row[0] not in used and row[week - CURRENT_WEEK + 1] < 0:
            # update the score, week, and add team to used
            score += row[week - CURRENT_WEEK + 1]
            week += 1
            used.append(row[0])

            # make the recursive call
            solve(used, score, week, grid, final_teams) == 1

            # remove the changes so you can continue the loop
            week -= 1
            score -= row[week - CURRENT_WEEK + 1]
            used.pop()


def main():
    df = pd.read_csv('data/Spread-10-5-21.csv', header=None)
    df.fillna(1000000, inplace=True)
    list_version = df.to_numpy().tolist()

    final_teams = []
    solve(list(), 0, CURRENT_WEEK, list_version, final_teams)
    print(f'Average Spread = {MIN_SCORE / (19-CURRENT_WEEK)}')
    print(f'Best Picks:')
    for i in range(18-CURRENT_WEEK + 1):
        print(f'  {i+CURRENT_WEEK}: {final_teams[i]}')


if __name__ == '__main__':
    main()