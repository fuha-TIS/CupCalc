import sqlite3

class dbHandler():
    def __init__(self):
        self.db = sqlite3.connect('calc.db')
    def createTables(self):
        self.db.executescript("""
            CREATE TABLE runners(
                id INTEGER PRIMARY KEY,
                first_name VARCHAR(20) NOT NULL,
                last_name VARCHAR(25) NOT NULL,
                club_id INTEGER,
                category_id INTEGER,
                FOREIGN KEY(category_id) REFERENCES categories(id)
                
            );
            CREATE TABLE categories(
                id INTEGER PRIMARY KEY,
                name VARCHAR(20) NOT NULL
            );
            CREATE TABLE clubs(
                id INTEGER PRIMARY KEY,
                name VARCHAR(20) NOT NULL
            );
            CREATE TABLE runs(
                id INTEGER PRIMARY KEY,
                name VARCHAR(20) NOT NULL,
                date_run DATE    NOT NULL,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                position INTEGER,
                status TEXT,
                season_id INTEGER,
                FOREIGN KEY(season_id) REFERENCES seasons(id),
                runner_id INTEGER,
                FOREIGN KEY(runner_id) REFERENCES runners(id),
            );
            CREATE TABLE results(
                id INTEGER PRIMARY KEY,
                runner_id INTEGER,
                FOREIGN KEY(runner_id) REFERENCES runners(id),
                run_id INTEGER,
                FOREIGN KEY(run_id) REFERENCES runs(id),
                points NUMERIC,
                position_run INTEGER
            );
            CREATE TABLE positions(
                position_season INTEGER,
                position_category INTEGER,
                season_id INTEGER,
                FOREIGN KEY(season_id) REFERENCES seasons(id),
                runner_id INTEGER,
                FOREIGN KEY(runner_id) REFERENCES runners(id),

            );

            CREATE TABLE seasons(
                id INTEGER PRIMARY KEY,
                name VARCHAR(20) NOT NULL,
                start_date DATE,
                end_date DATE
            );

        """)
    def checkAllTablesPresent(self):
        ans = True
        ans = ans && isRunnerExists()
        ans = ans && isCategoriesExists()
        ans = ans && isClubsExists()
        return ans

    def isRunnerExists(self):
        query = self.db.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='runners';
            """)
        if query.fetchone()[0] == 0:
            return False
        else:
            return True
    def isRunExists(self):
        query = self.db.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='runs';
            """)
        if query.fetchone()[0] == 0:
            return False
        else:
            return True
    def isCategoriesExists(self):
        query = self.db.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='categories';
            """)
        if query.fetchone()[0] == 0:
            return False
        else:
            return True
    def isClubsExists(self):
        query = self.db.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='clubs';
            """)
        if query.fetchone()[0] == 0:
            return False
        else:
            return True
    def isRunsExists(self):
        query = self.db.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='runs';
            """)
        if query.fetchone()[0] == 0:
            return False
        else:
            return True
    def isSeasonsExists(self):
        query = self.db.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='seasons';
            """)
        if query.fetchone()[0] == 0:
            return False
        else:
            return True
    def isPositionsExists(self):
        query = self.db.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='positions';
            """)
        if query.fetchone()[0] == 0:
            return False
        else:
            return True

    def addRunner(self, cc_card, first_name, last_name, club_id, category_id):
        self.db.execute("""
           INSERT INTO runners VALUES (?,?,?,?,?)
           """, (cc_card,first_name, last_name, club_id, category_id))
    def addCategory(self,name):
        self.db.execute("""
           INSERT INTO categories VALUES (?,?)
        """, (None, name))

    def addClub(self,name):
        self.db.execute("""
           INSERT INTO clubs VALUES (?,?)
        """, (None,name))

    def addRun(self, name, date_run, start_time, end_time, position, status, season_id, runner_id):
        self.db.execute("""
           INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?)
           """, (None,name,date_run,start_time,end_time,position,status,season_id,runner_id))
    def addSeason(self, name, start_date, end_date):
        self.db.execute("""
           INSERT INTO seasons VALUES (?,?,?,?)
           """, (None,name,start_date,end_date))
    def addPosition(self, position_season, position_category, season_id,runner_id):
        self.db.execute("""
           INSERT INTO positions VALUES (?,?,?,?,?)
       """, (None,position_season, position_category, season_id, runner_id))
    
    def exitHandler(self):
        self.db.commit()
        self.db.close()
