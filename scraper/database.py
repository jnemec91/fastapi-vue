import psycopg2
from psycopg2 import sql
from .beer import Beer, beer_from_list

class Database:
    def __init__(self, db: str, user: str, password: str, host: str, port: str) -> None:
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        print(f"Database '{db}' connected")

    def __str__(self) -> str:
        return self.db

    def __del__(self) -> None:
        if self.conn:
            self.conn.close()

    def connect(self) -> None:
        self.conn = psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()

    def create(self) -> None:
        self.connect()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS beer (
            id SERIAL PRIMARY KEY,
            name TEXT,
            style TEXT,
            abv TEXT,
            epm TEXT,
            ibu TEXT,
            brewery TEXT,
            location TEXT,
            description TEXT,
            url TEXT,
            image_url TEXT,
            rating TEXT
        )
        """)
        self.conn.commit()

    def fetch(self) -> list:
        self.cur.execute("SELECT * FROM beer")
        rows = self.cur.fetchall()
        
        # Convert rows to Beer objects
        for c, row in enumerate(rows):
            rows[c] = beer_from_list(row)

        return rows

    def find_fuzzy(self, beer: Beer) -> list:
        self.cur.execute("SELECT * FROM beer WHERE name LIKE %s", (f'%{beer.name}%',))
        rows = self.cur.fetchall()

        # Convert rows to Beer objects
        for c, row in enumerate(rows):
            rows[c] = beer_from_list(row)
        
        return rows

    def find_exact(self, beer: Beer) -> list:
        self.cur.execute("SELECT * FROM beer WHERE name = %s", (beer.name,))
        rows = self.cur.fetchall()

        # Convert rows to Beer objects
        for c, row in enumerate(rows):
            rows[c] = beer_from_list(row)
        
        return rows

    def insert(self, beer: Beer) -> bool:
        self.cur.execute("""
        INSERT INTO beer (name, style, abv, epm, ibu, brewery, location, description, url, image_url, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            beer.name, beer.style, beer.abv, beer.epm, beer.ibu,
            beer.brewery, beer.location, beer.description,
            beer.url, beer.image_url, beer.rating
        ))
        self.conn.commit()
        return True

    def remove(self, id: int) -> bool:
        self.cur.execute("DELETE FROM beer WHERE id = %s", (id,))
        self.conn.commit()
        return True

    def update(self, id: int, beer: Beer) -> bool:
        self.cur.execute("""
        UPDATE beer
        SET name = %s, style = %s, abv = %s, epm = %s, ibu = %s, brewery = %s,
            location = %s, description = %s, url = %s, image_url = %s, rating = %s
        WHERE id = %s
        """, (
            beer.name, beer.style, beer.abv, beer.epm, beer.ibu, beer.brewery,
            beer.location, beer.description, beer.url, beer.image_url, beer.rating, id
        ))
        self.conn.commit()
        return True
