import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute("""CREATE TABLE Client(
            ID_client INTEGER PRIMARY KEY AUTOINCREMENT,
            nume VARCHAR(40),
            adresa VARCHAR(200),
            telefon VARCHAR(15),
            mail VARCHAR(50),
            parola VARCHAR(50),
            card VARCHAR(50)
          )
        """)

c.execute("""CREATE TABLE Comanda(
          ID_comanda INTEGER PRIMARY KEY,
            ID_client INTEGER,
            metoda_platii VARCHAR(10),
            
            total REAL,
            data_comanda Date,
            FOREIGN KEY (ID_client) REFERENCES Client(ID_client) ON DELETE CASCADE
          )
          """)

c.execute("""CREATE TABLE Bilete(
            ID_bilete INTEGER PRIMARY KEY,
            ID_spectacol INTEGER,      
            cod_bilet INTEGER,
            tip_bilet VARCHAR(12),
            ID_comanda INTEGER,
            FOREIGN KEY (ID_spectacol) REFERENCES Spectacol(ID_spectacol) ON DELETE CASCADE,
            FOREIGN KEY (ID_comanda) REFERENCES Comanda(ID_comanda) ON DELETE CASCADE
)
          """)

c.execute("""CREATE TABLE Spectacol(
            ID_spectacol INTEGER PRIMARY KEY AUTOINCREMENT,
            nume_spectacol VARCHAR(70),
            data DATE,
            ora TIME,
            descriere_spectacol VARCHAR(70),
            ID_locatie INTEGER,
            bilete_max INTEGER,
            pret_bilet INTEGER,
            FOREIGN KEY (ID_locatie) REFERENCES Locatie(ID_locatie) ON DELETE CASCADE
        )
          """)

c.execute("""CREATE TABLE Locatie(
            ID_locatie INTEGER PRIMARY KEY AUTOINCREMENT,
            nume_locatie VARCHAR(70),
            adresa VARCHAR(100),
            capacitate INTEGER,
            detalii VARCHAR(150)
         )
          """)

c.execute("""CREATE TABLE SpectacolComediant(
            ID_spectacolcomediant INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_spectacol INTEGER,
            ID_comediant INTEGER,
            
            FOREIGN KEY (ID_spectacol) REFERENCES Spectacol(ID_spectacol) ON DELETE CASCADE,
            FOREIGN KEY (ID_comediant) REFERENCES Comediant(ID_comediant) ON DELETE CASCADE

          )
          """)

c.execute("""CREATE TABLE Comediant(
            ID_comediant INTEGER PRIMARY KEY AUTOINCREMENT,
            nume VARCHAR(40),
            telefon VARCHAR(15),
            mail VARCHAR(50),
            
            descriere_comediant VARCHAR(150),
            rating INT
          )
          """)