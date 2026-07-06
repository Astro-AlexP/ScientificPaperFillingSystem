import sqlite3

conn = sqlite3.connect('Papers.db')
c = conn.cursor()

# Create a new table
c.execute('''
    CREATE TABLE IF NOT EXISTS Papers (
        PaperID INTEGER PRIMARY KEY NOT NULL,
        Title TEXT NOT NULL,
        Summary TEXT NOT NULL,
        Link TEXT NOT NULL,
        DOI TEXT NOT NULL,
        TextRef TEXT NOT NULL
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        AuthorID INTEGER PRIMARY KEY NOT NULL,
        Initials TEXT NOT NULL,
        LastName TEXT NOT NULL,
        University TEXT NOT NULL
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS PaperAuthorsLink (
        PaperID INTEGER NOT NULL,
        AuthorID INTEGER NOT NULL,
        PRIMARY KEY (PaperID, AuthorID),
        FOREIGN KEY (PaperID) REFERENCES Papers(PaperID),
        FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Refs (
        ReferenceID INTEGER PRIMARY KEY NOT NULL,
        DOI TEXT NOT NULL,
        TextRef TEXT NOT NULL
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS PaperReferencesLink (
        PaperID INTEGER NOT NULL,
        ReferenceID INTEGER NOT NULL,
        PRIMARY KEY (PaperID, ReferenceID),
        FOREIGN KEY (PaperID) REFERENCES Papers(PaperID),
        FOREIGN KEY (ReferenceID) REFERENCES Refs(ReferenceID)
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Keywords (
        KeywordsID INTEGER PRIMARY KEY NOT NULL,
        Keyword TEXT NOT NULL
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS PaperKeywordsLink (
        PaperID INTEGER NOT NULL,
        KeywordsID INTEGER NOT NULL,
        PRIMARY KEY (PaperID, KeywordsID),
        FOREIGN KEY (PaperID) REFERENCES Papers(PaperID),
        FOREIGN KEY (KeywordsID) REFERENCES Keywords(KeywordsID)
    )
    ''')



conn.commit()
print("Database created")
conn.close()

