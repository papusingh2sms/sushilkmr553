1.START only main_window.py
2.SAVE to evaluate the points
3. to evaluate teams we have only ( match ) table in database
	for another matches you have to create a table same like match in database and put values in it
	CREATE TABLE [match_1] (
    Match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Player   TEXT,
    Scored   INTEGER,
    Faced    INTEGER,
    Fours    INTEGER,
    Sixes    INTEGER,
    Bowled   INTEGER,
    Maiden   INTEGER,
    Given    INTEGER,
    Wkts     INTEGER,
    Catches  INTEGER,
    Stumping INTEGER,
    Run_out  INTEGER
);