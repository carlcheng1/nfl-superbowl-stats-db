"""
Student name(s): Carl Cheng
Student email(s): carl@caltech.edu

******************************************************************************
Allows the client user to get an up-to-date view of each team's number of
Superbowl wins. Additionally allows the user to get other queries, such as
number of total touchdowns in the Superbowl by each team, and how many times 
each player played for a specific team in the Superbowl.
******************************************************************************
"""
import sys
import mysql.connector

import mysql.connector.errorcode as errorcode

DEBUG = False


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='sbclient',
          port='3306', # 8889 for MAMP
          password='clientpw',
          database='superbowl'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def team_wins_query():
    """
    Displays the view of number of Superbowl wins per team.
    """
    cursor = conn.cursor()
    sql = '''
SELECT * FROM team_superbowl_wins;
'''
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            (team, wins) = row
            print(f'{team}:', f'{wins}', 'wins')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred with view team_superbowl_wins')


def team_tds_query():
    """
    Finds the total number of passing touchdowns and rushing touchdowns
    each team has scored in the history of the Superbowl.
    """
    cursor = conn.cursor()
    sql = '''
SELECT team, SUM(passing_td) AS total_pass_tds,
    SUM(rushing_td) AS total_rush_tds
FROM game_stats NATURAL JOIN team
GROUP BY team_id;
'''
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            (team, pass_tds, rush_tds) = row
            print(f'{team}:', 
                  f'{pass_tds} total pass tds,', 
                  f'{rush_tds} total rush tds')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred with passing_td or rushing_td query')


def team_games_played_query():
    """
    Find all players who have played for a specific in the
    Superbowl and count the number of games they have played in.
    """
    param1 = input('Enter team abbreviation: (hint: try NWE or SDG) ')
    cursor = conn.cursor()
    sql = "SELECT name, COUNT(*) AS num_games \
FROM game_stats NATURAL JOIN player NATURAL JOIN team \
WHERE team.team = '%s' \
GROUP BY player_id;" % (param1, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            name, num_games = row
            print(f'{name}:', 
                  f'{num_games} games played')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred with count per player query')


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options client users can choose in the application, such as
    viewing Superbowl win counts of teams, viewing total touchdown counts of
    teams, viewing the number of games players have played for a specific team,
    etc.
    """
    print('What would you like to do? ')
    print('  (w) - view the superbowl win counts of teams')
    print('  (t) - view the total touchdown counts of teams')
    print('  (g) - view the number of games players have played for a given team')
    print('  (q) - quit')
    print()
    while True:
        ans = input('Enter an option: ').lower()
        if ans == 'q':
            quit_ui()
        elif ans == 'w':
            team_wins_query()
        elif ans == 't':
            team_tds_query()
        elif ans == 'g':
            team_games_played_query()
        else:
            print('Please select a valid option.')

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    conn = get_conn()
    main()
