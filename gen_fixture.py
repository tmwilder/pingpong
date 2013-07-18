import sqlite3
import subprocess
import os

DATETIME = "'1900-01-01 00:00:00'"
#Sqlite bool values for readability.
TRUE = 1
FALSE = 0 

def add_users(no_users, c):
    for user_id in range(1, no_users+1):
        s = "INSERT INTO auth_user ('password', 'last_login', 'is_superuser',"\
                                   "'username', 'first_name', 'last_name', "\
                                   "'email', 'is_staff', 'is_active', " \
                                   "'date_joined') " \
            "VALUES ('password', {1}, {2}, " \
                     "'user{0}', 'user{0}', 'user{0}', " \
                     "'test@test.com', {2}, {3}, " \
                     "{1})".format(user_id, DATETIME, FALSE, TRUE)
        c.execute(s)
    
        
def add_teams(no_teams, no_users, c):
    team_size = int(no_users/no_teams)
    team_id = 1
    for captain_id in range(1, no_users, team_size): 
        statement = ("INSERT INTO team (captain_id, name, creation_date) "
                     "VALUES ({0}, 'team{1}', {2})".format(captain_id, team_id, DATETIME))
        c.execute(statement)
        team_id += 1
    
    
def add_leagues(no_leagues, c):
    for league_id in range(1, no_leagues+1):
        #User league id as commissioner also. There are more leagues than users for our fixtures.
        statement = ("INSERT INTO league (location, sport, name, commissioner_id) "
                     "VALUES ('location{0}', 'sport{0}', 'league{0}', {0})".format(league_id))
        c.execute(statement)
    
    
def add_users_to_teams(no_teams, no_users, c):
    team_size = int(no_users/no_teams)
    team_id = 1
    for user_id in range(1, no_users+1):
        statement = ("INSERT INTO team_user (team_id, user_id) "
                     "VALUES ({0}, {1})".format(team_id, user_id))
        c.execute(statement)
        if user_id%team_size == 0:
            team_id += 1
        

def add_teams_to_leagues(no_teams, no_leagues, c):
    league_size = int(no_teams/no_leagues)
    league_id = 1
    counter = 0
    for team_id in range(1, no_teams+1):
        statement = ("INSERT INTO team_league (team_id, league_id, elo) "
                     "VALUES ({0}, {1}, {2})".format(team_id, league_id, 1500)
                    )
        c.execute(statement)
        if team_id%league_size == 0:
            team_id += 1
        counter += 1
        if counter == league_size:
            league_id += 1
            counter = 0
                     
    
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


def main(no_users=81,
         no_teams=27,
         no_leagues=3,
         target_file=".{0}pong_site{0}pong_app{0}fixtures{0}initial_data.json".format(os.sep)):
    #Setup connection.
    conn = sqlite3.connect('./db.sqlite3')
    c = conn.cursor()
    #Add data for all app tables.
    add_users(no_users, c)
    add_teams(no_teams, no_users, c)
    add_leagues(no_leagues, c)
    add_teams_to_leagues(no_teams, no_leagues, c)
    add_users_to_teams(no_teams, no_users, c)
    add_matches(no_teams, no_leagues, c)
    #Cleanup.
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
