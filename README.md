# NFL Superbowl Database
An NFL Superbowl game statistics database.  
Caltech CS 121: Intro to Relational Databases Final Project.  
Carl Cheng  

Data sourced from:  
https://www.kaggle.com/datasets/timoboz/superbowl-history-1967-2020  
https://www.kaggle.com/datasets/mattop/nfl-superbowl-offensive-statistics-19662021  
https://www.kaggle.com/datasets/kendallgillies/nflstatistics (to get player birthdays, colleges, positions)  

Use the preprocessed CSVs I provide in link-to-data.txt. Put them in a folder called 'data' in the working tree directory (see load-data.sql).

To load the database from the command-line, run these commands:
$ [cd into final_project]
$ [start mySQL, e.g. with mysql --local-infile=1 -u root -p]
mysql> source setup.sql;
mysql> source load-data.sql;
mysql> source setup-passwords.sql;
mysql> source setup-routines.sql;
mysql> source grant-permissions.sql;
mysql> source queries.sql;

To run the Python application, run these commands:
mysql> quit;

$ python3 app-client.py

OR

$ python3 app-admin.py

Please log in with the following user/passwords for app-admin.py:
    Username, Password:
    sbadmin, password
    carl, letmein

To use the client app:
    (w) - view the superbowl win counts of teams
    (t) - view the total touchdown counts of teams
    (g) - view the number of games players have played for a given team
    (q) - quit the app

To use the admin app:
    (l) - log in using a username, password
    (i) - insert a new Superbowl game into the database
    (q) - quit the app

