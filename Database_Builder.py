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
        TextRef TEXT NOT NULL,
        NumOfRefs INTEGER NOT NULL,
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        AuthorID INTEGER PRIMARY KEY NOT NULL,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL
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
    CREATE TABLE IF NOT EXISTS Institutions (
        InstitutionID INTEGER PRIMARY KEY NOT NULL,
        Name TEXT NOT NULL
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS AuthorsInstitutionLink (
        InstitutionID INTEGER NOT NULL,
        AuthorID INTEGER NOT NULL,
        PRIMARY KEY (InstitutionID, AuthorID),
        FOREIGN KEY (InstitutionID) REFERENCES Institutions(InstitutionID),
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
        KeywordID INTEGER PRIMARY KEY NOT NULL,
        Keyword TEXT NOT NULL
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS PaperKeywordsLink (
        PaperID INTEGER NOT NULL,
        KeywordID INTEGER NOT NULL,
        PRIMARY KEY (PaperID, KeywordID),
        FOREIGN KEY (PaperID) REFERENCES Papers(PaperID),
        FOREIGN KEY (KeywordID) REFERENCES Keywords(KeywordID)
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Edges (
            Paper1ID INTEGER NOT NULL,
            Paper2ID INTEGER NOT NULL,
            PRIMARY KEY (Paper1ID, Paper2ID),
            FOREIGN KEY (Paper1ID) REFERENCES Papers(PaperID),
            FOREIGN KEY (Paper2ID) REFERENCES Papers(PaperID)
    )
    ''')



conn.commit()
print("Database created")
conn.close()

