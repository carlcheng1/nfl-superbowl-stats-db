CREATE DATABASE superbowl;
USE superbowl;

DROP TABLE IF EXISTS game_stats;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    -- player id (integer >= 0)
    player_id INT,
    -- player name
    name VARCHAR(40),
    -- player position
    position VARCHAR(3),
    -- player birthday
    birthday DATE,
    -- player college
    college VARCHAR(100),
    PRIMARY KEY (player_id)
);

CREATE TABLE team ( 
    -- team id
    team_id INT,
    -- team abbreviation (e.g. BAL)
    team VARCHAR(3),
    PRIMARY KEY (team_id)
);

CREATE TABLE game (
    -- game id (e.g. 2002)
    game_id YEAR,
    -- SB title (roman numerals, e.g. LIV (54))
    sb VARCHAR(40),
    -- team_id of winning team
    winner_id INT,
    -- pts scored by winning team
    winner_pts INT,
    -- team_id of losing team
    loser_id INT,
    -- pts scored by losing team
    loser_pts INT,
    -- location of Superbowl: stadium, city, state
    stadium VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(50),
    PRIMARY KEY (game_id),
    FOREIGN KEY (winner_id) REFERENCES team(team_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (loser_id) REFERENCES team(team_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE game_stats ( 
    -- game id (e.g. 2002)
    game_id YEAR,
    -- player id (integer >= 0)
    player_id INT,
    -- team that the player played for in the game [game_id]
    team_id INT,
    -- per-game offensive statistics of player in game_id:
    completions INT,
    pass_attempts INT,
    passing_yards INT,
    passing_td INT,
    interception INT,
    times_sacked INT,
    sack_yards INT,
    longest_pass INT,
    qbr NUMERIC(4, 1),
    rush_attempts INT,
    rushing_yards INT,
    rushing_td INT,
    longest_run INT,
    receptions INT,
    receiving_yards INT,
    receiving_td INT,
    longest_reception INT,
    fumble INT,
    fumbles_lost INT,
    PRIMARY KEY (game_id, player_id, team_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (player_id) REFERENCES player(player_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_pass_td ON game_stats(team_id, passing_td);
CREATE INDEX idx_rush_td ON game_stats(team_id, rushing_td);
CREATE INDEX idx_receiving_td ON game_stats(team_id, receiving_td);
