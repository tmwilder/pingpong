import sqlite3
import subprocess
import os

DATETIME = "'2013-01-01 01:01:01'"

def add_players(no_players, c):
    for player_id in range(1, no_players+1):
        statement = ("INSERT INTO player (player_name, player_nick, join_date) "
                     "VALUES ('player{0}', 'player{0}', {1})".format(player_id, DATETIME))
        c.execute(statement)
    
        
def add_teams(no_teams, no_players, c):
    team_size = int(no_players/no_teams)
    team_id = 1
    for captain_id in range(1, no_players, team_size): 
        statement = ("INSERT INTO team (captain_id, name, creation_date) "
                     "VALUES ({0}, 'team{1}', {2})".format(captain_id, team_id, DATETIME))
        c.execute(statement)
        team_id += 1
    
    
def add_leagues(no_leagues, c):
    for league_id in range(1, no_leagues+1):
        statement = ("INSERT INTO league (location, sport) "
                     "VALUES ('location{0}', 'sport{0}')".format(league_id))
        c.execute(statement)
    
    
def add_players_to_teams(no_teams, no_players, c):
    team_size = int(no_players/no_teams)
    team_id = 1
    for player_id in range(1, no_players+1):
        statement = ("INSERT INTO team_player (team_id, player_id) "
                     "VALUES ({0}, {1})".format(team_id, player_id))
        c.execute(statement)
        if player_id%team_size == 0:
            team_id += 1
        

def add_teams_to_leagues(no_teams, no_leagues, c):
    league_size = int(no_teams/no_leagues)
    league_id = 1
    for team_id in range(1, no_teams+1):
        statement = ("INSERT INTO team_league (team_id, league_id, elo) "
                     "VALUES ({0}, {1}, {2})".format(team_id, league_id, 1500)
                    )
        c.execute(statement)
        if team_id%league_size == 0:
            team_id += 1
                     
    
def add_matches(no_teams, no_leagues, c):
    match_id = 1
    for team1 in range(1, no_teams+1):
        for team2 in range(1, no_teams+1):
            for league in range(1, no_leagues+1):
                if team1 == team2:
                    continue
                statement = ("INSERT INTO match "
                                "(team1_id, team2_id, result, start_elo1,"
                                " start_elo2, league_id, start_time, match_info) "
                             "VALUES ({0},{1},{2},{3},{4},{5},{6},'{7}')"
                            ).format(team1, team2, 1, 1500, 1500,
                                     league, "'2013-01-01 00:00:00'",
                                     match_id)
                c.execute(statement)
                match_id += 1


def main(no_players=81,
         no_teams=27,
         no_leagues=3,
         target_file=".{0}pong_site{0}pong_app{0}fixtures{0}initial_data.json".format(os.sep)):
    #Setup connection.
    conn = sqlite3.connect('./db.sqlite3')
    c = conn.cursor()
    #Add data for all app tables.
    add_players(no_players, c)
    add_teams(no_teams, no_players, c)
    add_leagues(no_leagues, c)
    add_teams_to_leagues(no_teams, no_leagues, c)
    add_players_to_teams(no_teams, no_players, c)
    add_matches(no_teams, no_leagues, c)
    #Cleanup.
    conn.commit()
    conn.close()
    #TODO figure out '>' error.
    #command = ["python", ".{0}pong_site{0}manage.py".format(os.sep),
    #           "dumpdata", "--format=json", "pong_app", ">", target_file]
    #subprocess.call(command)


if __name__ == "__main__":
    main()
