import random
from tabnanny import check

def num_checker(func):
    def wrapper(num): 
        try:
            num = int(num)
        except:
            return False
        result = func(num)
        return result
    return wrapper

@num_checker
def number_of_team_checker(value):
    value = int(value)
    if value < 2:
        return False, value
    elif value % 2 > 0:
        return False, value
    
    return True

def team_name_checker(value):
    value = value.split(' ')
    value_len = len(value)
    if value_len == 1:
        if len(value[0]) == 1:
            return False, len(value[0])          
    elif value_len > 2:
        return False, value_len 
    return True


def number_of_games_per_team_check(num_team, value):
    try:
        value = int(value)
    except:
        return False
    num_team = num_team - 1
    if value < num_team:
        return False
    return True

def num_of_win(max_game, value):
    try:
        value = int(value)
    except:
        return False, value
    if value < 0:
        return False, value
    elif value > max_game:
        return False, value
    return True

def local_generator(teams):
    teams = list(teams)
    end = -1
    for num in range(int(len(teams)/2)):
        print(f"Home: {teams[num]} VS Away: {teams[end - num]}")


def game_generator():
    teams = [] 
    team_wins = []
    team_win_dict = {}

    games = input("Enter the number of teams in the tournament: ")
    while True:
        check = number_of_team_checker(games)
        if check == True:
            games = int(games)
            break
        if check[1] > 2:
            print("Enter an even number of teams.")
        else:
            print("The minimum number of teams is 2, try again.")
        games = input("Enter the number of teams in the tournament: ")

    for num in range(1, games+1):
        team = input(f"Enter the name for team #{num}: ")
        check = team_name_checker(team)
        while True:
            if check == True:
                break
            if check[0] == False and check[1] == 1:
                print("Team names must have at least 2 characters, try again.")
            else:
                print("Team names may have at most 2 words, try again.")  
            team = input(f"Enter the name for team #{num}: ")
            check = team_name_checker(team)
        teams.append(team)

    
    no_games = input("Enter the number of games played by each team: ")
    check = number_of_games_per_team_check(games, no_games)
    while True:
        if check == True:
            no_games = int(no_games)
            break
        print(f"Invalid number of games. Each team plays each other at least once in the regular season, try again.")
        no_games = input("Enter the number of games played by each team: ")
        check = number_of_games_per_team_check(games, no_games)

    for team in teams:
        no_wins = input(f"Enter the number of wins Team {team} had: ")
        check = num_of_win(no_games, no_wins)
        while True:
            if check == True:
                break
            if check[1] < 0:
                print("The minimum number of wins is 0, try again.")
            else:
                print(f"The maximum number of wins is {no_games}, try again.")
            no_wins = input(f"Enter the number of wins Team {team} had: ")
            check = num_of_win(no_games, no_wins)
        team_wins.append(no_wins)

    for team_win in zip(teams, team_wins):
        team_win_dict[team_win[0]] =  team_win[1]
    team_win_dict = dict(sorted(team_win_dict.items(), key = lambda x: x[1]))

    local_generator(team_win_dict)

game_generator()
