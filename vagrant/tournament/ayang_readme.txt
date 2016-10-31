TOURNAMENTS README
by Andy Yang

Tournament.sql

In the sql file, I wanted to automate the process of creating the database "tournament" and the corresponding tables. There are two tables named "players" and "matches". In the "players" table, I have two columns: an id (serial) and name (text) with the id being a primary key. In the "matches" table, I have three columns: id (a serial primary key), winner (integer), and loser (integer). Both "winner" and "loser" are foreign keys to the primary key "id" of the "players" table.

In the file, there is also a view, "player_standing" because it is a longer query. The query results in four columns: id, name, wins, and matches. "ID" and "name" are taken from the "players" table, while "wins" and "matches" are counted from the "matches" table. "Matches" is the result of the count of both the "winner" and "loser" columns for any player. The results are grouped by "id" and are in descending order of "wins".

This file can be imported from PSQL by using the \i tournament.sql command.

Tournament.py

This file contains all the functions that are necessary to run a Swiss-Pairings style tournament.

connect() function:
This function attempts to connect to the tournament database and create a cursor to be used. These are returned if this is successfuly. Otherwise, an exception is thrown with the following message: "Database/cursor was unable to be accessed". 

This function is called in all subsequent functions. In each function that it is called, the database is closed at the end.

deleteMatches() function:
This function creates and executes a query that deletes all rows from the "matches" table.

deletePlayers() function:
This funciton creates and executes a query that deletes all rows form the "players" table.

registerPlayer(name) function:
This function takes in a string "name" which is in executing a query to insert a row into the "players" table. To avoid sql injections, parameterized queries are used. The change is then committed.

playerStandings():
This function returns a list of tuples that contain the following information: player id, player name, number of wins, and total number of matches played by player. This is done by executing a query that calls on the preconfigured view "player standing". The results of this query are then loaded into the list of tuples, using a for-loop.

reportMatch(winner, loser):
This function takes two strings "winner" and "loser" and adds them as entries into "matches" table, using a parameterized query. The changes are then committed.

swissPairings():
This function returns a list of tuples containing the following information: player 1's id and name, and player 2's id and name. "Player 1" and "Player 2" correspond the players for the next match. This function takes advantage of the playerStandings() function which returns a list all players ordered by the number of wins. The swissPairings() function uses a while-loop to go through the list from playerStandings and obtains two names and ids at a time and adds them to the list of tuples to be returned (swiss_pairings). The while-loop uses a counter that is incremented by 2 with every iteration of the while-loop. The while-loop is executed as long as the counter is less than the number of players in the "players" table. The list is then returned.