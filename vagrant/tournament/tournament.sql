-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dAShes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players(
  id serial PRIMARY KEY,
  name text);
CREATE TABLE matches(
  id serial PRIMARY KEY,
  winner INTEGER REFERENCES players(id),
  loser INTEGER REFERENCES players(id));

  -- Create view to generate player standings
CREATE VIEW player_standing AS 
select a.id, a.name, COUNT(b.winner) AS wins,
	(COUNT(b.winner) + COUNT(c.loser)) AS matches
	FROM players AS a
	LEFT JOIN matches AS b
	on a.id = b.winner
	LEFT JOIN matches AS c
	ON a.id = c.loser
	GROUP BY a.id
    ORDER BY wins;