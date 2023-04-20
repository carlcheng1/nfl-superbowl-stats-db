"""
Student name(s): Carl Cheng
Student email(s): carl@caltech.edu

******************************************************************************
Allows the admin to log in and, once logged in, insert new games into the
database. We implement only adding games for simplicity since we have a view,
procedure, and trigger specifically for adding games, but the same could be 
done for game_stats (above and beyond/future work).
******************************************************************************
"""

import sys
import mysql.connector

import mysql.connector.errorcode as errorcode

DEBUG = False
# Logged in flag
is_logged_in = False

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
          user='sbadmin',
          port='3306', # 8889 for MAMP
          password='adminpw',
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
def insert_game():
    """
    Inserts a new game into the database. Provide the game_id, SB title,
    winner_id, winner_pts, loser_id, loser_pts when prompted. Shows the view 
    team_superbowl_wins right after to show that the database is indeed updated
    .
    """
    game_id = input('Enter game id: ')
    sb = input('Enter SB title (i.e. roman numerals): ')
    winner_id = input('Enter team id of winner: ')
    winner_pts = input('Enter pts scored by winner: ')
    loser_id = input('Enter team id of loser: ')
    loser_pts = input('Enter pts scored by loser: ')
    param1 = (game_id, sb, winner_id, winner_pts, loser_id, loser_pts)
    cursor = conn.cursor()
    sql = "CALL insert_game(%s,'%s',%s,%s,%s,%s);" % param1
    try:
        cursor.execute(sql)
        conn.commit()
        # row = cursor.fetchone()
        print('Row inserted\n')
        cursor.execute("SELECT * FROM team_superbowl_wins;")
        rows = cursor.fetchall()
        for row in rows:
            (team, wins) = row
            print(f'{team}:', f'{wins}', 'wins')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, could not insert into \
                        game by calling insert_game')



# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
def log_in():
    """
    Logs into the database with a username and password.
    """
    cursor = conn.cursor()
    username = input('Enter username: ')
    pw = input('Enter password: ')
    sql = "SELECT authenticate('%s','%s');" % (username, pw)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows[0][0] == 1:
            global is_logged_in
            is_logged_in = True
        else:
            print('Invalid username and/or password.')
        
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, could not log in')


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------

def show_options():
    """
    Displays options specific for admins, such as inserting new data into game,
    logging in, etc.
    """
    print('What would you like to do? ')
    print('  (l) - log in')
    print('  (i) - insert a new game')
    print('  (q) - quit')
    print()
    while True:
        ans = input('Enter an option: ').lower()
        if ans == 'q':
            quit_ui()
        elif ans == 'l':
            if is_logged_in:
                print('You are already logged in.')
            else:
                log_in()
        elif ans == 'i':
            if is_logged_in:
                insert_game()
            else:
                print('Please log in first.')
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
