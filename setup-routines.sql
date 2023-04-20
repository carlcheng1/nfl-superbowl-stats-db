
-- UDF to compute the completion percentage of a player for their entire
-- Superbowl history
DROP FUNCTION IF EXISTS completion_pct;
DELIMITER !
CREATE FUNCTION completion_pct(player_id INT)
RETURNS NUMERIC(3,2)
BEGIN
    DECLARE completions INT;
    DECLARE pass_attempts INT;
    DECLARE comp_pct NUMERIC(3,2);
    
    SELECT SUM(completions), SUM(pass_attempts)
    INTO completions, pass_attempts
    FROM game_stats
    WHERE player_id = player_id;
    
    SET comp_pct = completions / pass_attempts;
    
    RETURN comp_pct;
END !
DELIMITER ;

-- Procedure to update the stadium and city of a game
DROP PROCEDURE IF EXISTS update_game_location;
DELIMITER !
CREATE PROCEDURE update_game_location(game_id YEAR, stadium VARCHAR(100),
                                      city VARCHAR(100), state VARCHAR(50))
BEGIN
    UPDATE game
    SET stadium = stadium, city = city, state = state
    WHERE game_id = game_id;
END !
DELIMITER ;

-- Procedure to insert a new game
DROP PROCEDURE IF EXISTS insert_game;
DELIMITER !
CREATE PROCEDURE insert_game(game_id YEAR, 
                             sb VARCHAR(40),
                             winner_id INT,
                             winner_pts INT,
                             loser_id INT,
                             loser_pts INT)
BEGIN
    INSERT INTO game (game_id, 
                      sb, 
                      winner_id, 
                      winner_pts, 
                      loser_id, 
                      loser_pts)
    VALUES (game_id, 
            sb, 
            winner_id, 
            winner_pts, 
            loser_id, 
            loser_pts);
END !
DELIMITER ;

-- Materialized view, procedure, and trigger for managing view of Superbowl 
-- wins per team.
--
-- Table for inserting into team_superbowl_wins materialized view
DROP TABLE IF EXISTS mv_team_superbowl_wins;
CREATE TABLE mv_team_superbowl_wins ( 
    team_id INT, 
    wins INT,
    PRIMARY KEY (team_id)
);

-- Find wins and insert into team_superbowl_wins mv table
-- INSERT INTO mv_team_superbowl_wins ( 
--     (SELECT winner_id AS team_id, COUNT(*) AS wins
--     FROM game
--     GROUP BY winner_id)
--     NATURAL LEFT JOIN
--     (SELECT loser_id AS team_id, 0 AS wins
--     FROM game
--     GROUP BY loser_id)
-- );
INSERT INTO mv_team_superbowl_wins (
    SELECT team_id, SUM(wins) AS wins
    FROM (
        SELECT winner_id AS team_id, COUNT(*) AS wins
        FROM game
        GROUP BY winner_id
        UNION ALL
        SELECT loser_id AS team_id, 0 AS wins
        FROM game
        GROUP BY loser_id
    ) AS subquery
    GROUP BY team_id
);

-- Create materialized view for team_superbowl_wins
DROP VIEW IF EXISTS team_superbowl_wins;
CREATE VIEW team_superbowl_wins AS 
    SELECT team, wins 
    FROM mv_team_superbowl_wins NATURAL JOIN team ORDER BY wins DESC;

-- Procedure to update view whenever game is inserted into game
DROP PROCEDURE IF EXISTS sp_team_wins_update;
DELIMITER !
CREATE PROCEDURE sp_team_wins_update(
    team_id INT
)
BEGIN
    INSERT INTO mv_team_superbowl_wins (team_id, wins)
    VALUES (team_id, 1)
    ON DUPLICATE KEY UPDATE
        wins = wins + 1;
END !

-- Trigger to handle inserts into game for team_superbowl_wins
DROP TRIGGER IF EXISTS trg_game_insert;
CREATE TRIGGER trg_game_insert AFTER INSERT 
    ON game FOR EACH ROW 
BEGIN 
    CALL sp_team_wins_update(NEW.winner_id);
END !
DELIMITER ;

