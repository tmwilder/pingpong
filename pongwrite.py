import sqlite3


conn = sqlite3.connect('./db.sqlite3')

c = conn.cursor()


for team1 in range(9):
    for team2 in range(9):
        for league in range(3):
            team1 += 1
            team2 += 1
            league += 1
            statement = ("INSERT INTO match "
                            "(team1_id, "
                            "team2_id, "
                            "result, "
                            "start_elo1, "
                            "start_elo2, "
                            "league_id, "
                            "start_time, "
                            "match_info "
                            ") "
                         "VALUES "
                            "({0}, " 
                             "{1}, "
                             "{2}, "
                             "{3}, "
                             "{4}, "
                             "{5}, "
                             "{6}, "
                             "{7} "
                             ")").format(team1, team2, 1, 1500, 1500,
                                         league, "'2013-01-01 00:00:00'",
                                       "'A match ocurred! Huzzah!'")
            print repr(statement)
            c.execute(statement)
        
conn.commit()
conn.close()

