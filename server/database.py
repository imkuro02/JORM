import sqlite3

class DataBase:
    def __init__(self):
        # Connect to the database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Create the users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        ''')

        # Create the actors table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS actors (
            username TEXT PRIMARY KEY,
            hp INTEGER DEFAULT 0,
            mp INTEGER DEFAULT 0,
            max_hp INTEGER DEFAULT 0,
            max_mp INTEGER DEFAULT 0,
            exp INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            crit_chance REAL DEFAULT 0,
            dodge_chance REAL DEFAULT 0,

            str INTEGER DEFAULT 0,
            agi INTEGER DEFAULT 0,
            int INTEGER DEFAULT 0,

            FOREIGN KEY(username) REFERENCES users(username)
        )
        ''')

        # Create the items table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            username TEXT,
            item_name TEXT,
            item_quantity INTIGER,
            FOREIGN KEY(username) REFERENCES users(username)
        )
        ''')

        # Create the items table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            username TEXT,
            item_name TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
        ''')

    def create_account(self,username,password):
        account_exists = len(self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchall()) == 1
        if not account_exists:
            self.cursor.execute('''
                INSERT INTO users (
                    password, username
                ) VALUES (?, ?)
                ''', (password,username))
            print('creating new account')
        else:
            print('account already exists')
        self.conn.commit()

    def get_account(self,username,password):
        account = self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username,password)).fetchall()
        return account

    def save_player(self,actor):
        _stats = tuple(actor.stats.values())
        _actor = _stats + (actor.name,) 
        self.cursor.execute('''
            INSERT INTO actors (
                hp, mp, max_hp, max_mp, exp, points, crit_chance, dodge_chance,
                str, agi, int, username
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
                hp = excluded.hp,
                mp = excluded.mp,
                max_hp = excluded.max_hp,
                max_mp = excluded.max_mp,
                exp = excluded.exp,
                points = excluded.points,
                crit_chance = excluded.crit_chance,
                dodge_chance = excluded.dodge_chance,
                str = excluded.str,
                agi = excluded.agi,
                int = excluded.int

            ''', _actor)
        
        
        self.cursor.execute('DELETE FROM items WHERE username = ?', (actor.name,))
        self.cursor.execute('DELETE FROM equipment WHERE username = ?', (actor.name,))
        

        for item in actor.inventory:
            self.cursor.execute('INSERT INTO items (username, item_name, item_quantity) VALUES (?, ?, ?)', (actor.name,item,actor.inventory[item]))
            #self.cursor.execute('SELECT * FROM items')
            #items = self.cursor.fetchall()
            #print(items)

        for eq in actor.equipment:
            self.cursor.execute('INSERT INTO equipment (username, item_name) VALUES (?, ?)', (actor.name,eq))

        self.conn.commit()


    def load_player(self,username):
        stats = {}
        inventory = {}
        equipment = []
        _stats = self.cursor.execute('SELECT * FROM actors WHERE username = ?',(username,)).fetchall()
        if _stats == []: return None
        _inventory = self.cursor.execute('SELECT * FROM items WHERE username = ?',(username,)).fetchall()
        _equipment = self.cursor.execute('SELECT * FROM equipment WHERE username = ?',(username,)).fetchall()
        for item in _inventory:
            inventory[item[1]] = item[2]

        stat_names = '''username, hp, mp, max_hp, max_mp, exp, points, crit_chance, dodge_chance, str, agi, int'''.split(', ')
        stats =  dict(zip(stat_names, _stats[0]))
        del stats['username']


        equipment = [item[1] for item in _equipment]
        #print(stats, inventory, equipment)
        #print(stats)
        return {'stats': stats, 'inventory': inventory, 'equipment':equipment}
        

    def close(self):
        self.conn.commit()
        self.conn.close()
