#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
	db = psycopg2.connect("dbname=tournament")
	c = db.cursor()
	return db, c
    except:
	print ("Database/cursor was unable to be accessed")


def deleteMatches():
    """Remove all the match records from the database."""
    
    """ create database and cursor from connect()"""
    db, c = connect()
    
    query = "delete from matches"
    c.execute(query)
    db.commit()
    db.close()
	
	

def deletePlayers():
    """Remove all the player records from the database."""
	
    """ create database and cursor from connect()"""
    db, c = connect()

    query = "delete from players"
    c.execute(query)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    
    """ create database and cursor from connect()"""
    db, c = connect()

    query = "select count(*) as num from players"
    c.execute(query)
    count = c.fetchone()[0]
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    """ create database and cursor from connect()"""
    db, c = connect()
    
    query = "insert into players(name) values (%s)"
    
    c.execute(query, (name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    """ create database and cursor from connect()"""
    db, c = connect()

    """create list of tuples to be returned, p_stand"""
    p_stand = []
    
    """generate desired results from player_standing view"""
    query = "select * from player_standing"
    c.execute(query)
    count_query = countPlayers()
    stand_temp = c.fetchall()
    
    """add results from query to p_stand as tuples"""
    for row in stand_temp:
        temp = (row[0], row[1], row[2],row[3])
        p_stand.append(temp)
    
    db.close()
    return p_stand

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    """ create database and cursor from connect()"""
    db, c = connect()
    
    query = "insert into matches(winner, loser) values (%s,%s)" 
    entries = (winner,loser)
    c.execute(query, entries)
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    """ create database and cursor from connect()"""
    db, c = connect()
    
    p_count = countPlayers()
    ps = playerStandings()
    swiss_pairings = []
    i = 0

    while (i < p_count):
        temp = (ps[i][0],ps[i][1],ps[i+1][0],ps[i+1][1])
        swiss_pairings.append(temp)
        i += 2

    db.close()
    return swiss_pairings
