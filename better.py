import pandas as pd
import numpy as np

class data:
    score = 1000
    final_teams = []

def solve(grid, current_score, current_index, teams, data, cache, teams_used):
    # check cache to see if we've already used this combo of teams
    if teams_used in cache:
        if current_score < cache[teams_used]:
            cache[teams_used] = current_score
        else:
            return
    else:
        cache[teams_used] = current_score

    # end condition, we've gone through all columns
    if current_index == 13:
        if current_score < data.score:
            data.score = current_score
            data.final_teams = teams.copy()
        return

    for i in range(len(grid)):
        if grid[i][current_index] != 1000 and (current_score+grid[i][current_index]) < data.score:
            temp_grid = grid.copy()
            temp_grid[i] = 1000
            teams_used |= (1 << i)
            name = grid[i][0]
            teams.append(name)
            solve(temp_grid, current_score + grid[i][current_index], current_index+1, teams, data, cache, teams_used)
            teams_used ^= (1 << i)
            teams.pop()

if __name__ == '__main__':
    df = pd.read_csv('data/grid-9-8-22.csv')
    df.fillna(1000, inplace=True)

    grid = df.to_numpy()

    # de facto remove all non-favored teams from consideration
    for i in range(grid.shape[0]):
        for j in range(1, grid.shape[1]):
            if grid[i][j] >= 0:
                grid[i][j] = 1000

    # now make everything positive
    adj = np.min(grid[:, 1:])
    grid[:, 1:] += abs(np.min(grid[:, 1:]))

    cache = {}
    data_class = data()
    solve(grid, 0, 1, [], data_class, cache, 0)
    print(f'{data_class.final_teams} {data_class.score + (adj * len(data_class.final_teams))}')