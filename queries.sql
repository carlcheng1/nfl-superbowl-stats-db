-- Get a list of all teams who have won the superbowl and count the number
-- of times they have won
SELECT team, COUNT(*) AS num_wins
FROM team, game 
WHERE team_id = winner_id
GROUP BY team;

-- Find all players that have had at least 400 passing yards and 3
-- touchdowns with a QBR >= 100 in the Superbowl, and list the games and
-- their respective stats.
SELECT name, game_id, passing_yards, passing_td, rushing_td, qbr
FROM game_stats NATURAL JOIN player
WHERE passing_yards >= 400 AND (passing_td + rushing_td) >= 3 AND qbr >= 100;

-- Relational Algebra query 1
-- Find all players who have played for the New England Patriots in the
-- superbowl and count the number of games they have played in
SELECT name, COUNT(*) AS num_games
FROM game_stats NATURAL JOIN player NATURAL JOIN team
WHERE team.team = 'NWE'
GROUP BY player_id;

-- Relational Algebra query 2
-- Find the total number of passing touchdowns and rushing touchdowns
-- each team has scored in the history of the Superbowl
--
-- Used primarily to test the indexes 
SELECT team, SUM(passing_td) AS total_pass_tds,
    SUM(rushing_td) AS total_rush_tds
FROM game_stats NATURAL JOIN team
GROUP BY team_id;
