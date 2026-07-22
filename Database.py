import sqlite3
import base64
from Paper_Info import getCredentials, fetchNumOfRefs


def savePaper(Title, Authors, DOI, Keywords, Summary, filePath, PaperData, fileData):
    conn = sqlite3.connect('Papers.db')
    c = conn.cursor()
    filePath = './Papers/' + filePath
    content_type, content_string = fileData.split(",")
    decoded_bytes = base64.b64decode(content_string)
    with open(filePath, 'wb') as f:
        f.write(decoded_bytes)

    bibtex = generateBibtex(PaperData)
    PaperID = writeToPapers(c, Title, Summary, filePath, DOI, bibtex)
    writeToAuthors(c, PaperID, Authors, PaperData['Institutions'])
    writeToRefs(c, PaperID, PaperData['refDOI'], PaperData['formatedRef'])
    writeToKeywords(c, PaperID, Keywords)

    conn.commit()

    findEdges(c)
    updateNumOfRefs(c)

    conn.commit()

def generateBibtex(data):
    return 'temp'

def updateNumOfRefs(c):
    papers = c.execute('''SELECT DOI FROM Papers''').fetchall()

    for paper in papers:
        creds = getCredentials()

        numOfRefs = fetchNumOfRefs(paper[0], creds)

        c.execute('''UPDATE Papers SET NumOfRefs = ? WHERE DOI = ?''', (numOfRefs, paper[0]))


def writeToPapers(c, Title, Summary, Link, DOI, Bibtex):
    ids = c.execute('''SELECT PaperID FROM Papers''').fetchall()
    newid = len(ids) + 1

    c.execute('''INSERT INTO Papers(PaperID, Title, Summary, Link, DOI, TextRef, NumOfRefs) Values (?, ?, ?, ?, ?, ?, ?)''', (newid, Title, Summary, Link, DOI, Bibtex, 0))

    return newid

def writeToAuthors(c, PaperID, Authors, Institutions):
    AuthorList = [item.strip() for item in Authors.split(",")]
    DatabaseAuthors = c.execute('''SELECT AuthorID, FirstName, LastName FROM Authors''').fetchall()

    addedAuthors = 0
    for author in AuthorList:
        authorFound = False
        for recordedAuthor in DatabaseAuthors:
            if author == recordedAuthor[1] + ' ' + recordedAuthor[2]:
                c.execute('''INSERT INTO PaperAuthorsLink(PaperID, AuthorID) Values (?, ?)''', (PaperID, recordedAuthor[0]))
                authorFound = True

        if not authorFound:
            addedAuthors += 1
            splitAuthors = author.split(' ')
            firstName = splitAuthors[0]
            lastName = ''
            for name in splitAuthors[1:]:
                lastName += name + ' '
            c.execute('''INSERT INTO Authors(AuthorID, FirstName, LastName) Values (?, ?, ?)''', (len(DatabaseAuthors) + addedAuthors, firstName, lastName))
            writeToInstitutions(c, len(DatabaseAuthors) + addedAuthors, Institutions[author])
            c.execute('''INSERT INTO PaperAuthorsLink(PaperID, AuthorID) Values (?, ?)''', (PaperID, len(DatabaseAuthors) + addedAuthors))


def writeToInstitutions(c, AuthorID, Institutions):
    DatabaseInsts = c.execute('''SELECT InstitutionID, Name FROM Institutions''').fetchall()
    addedInstitutions = 0
    for Institution in Institutions:
        InstitutionFound = False
        for recordedInst in DatabaseInsts:
            if Institution == recordedInst[1]:
                c.execute('''INSERT INTO AuthorsInstitutionLink(InstitutionID, AuthorID) Values (?, ?)''',
                          (recordedInst[0], AuthorID))
                InstitutionFound = True

        if not InstitutionFound:
            addedInstitutions += 1
            c.execute('''INSERT INTO Institutions(InstitutionID, Name) Values (?, ?)''',
                      (len(DatabaseInsts) + addedInstitutions, Institution))
            c.execute('''INSERT INTO AuthorsInstitutionLink(InstitutionID, AuthorID) Values (?, ?)''',
                      (len(DatabaseInsts) + addedInstitutions, AuthorID))

def writeToRefs(c, PaperID, DOI, textRef):
    DatabaseRefs = c.execute('''SELECT ReferenceID, DOI, TextRef FROM Refs''').fetchall()
    addedRefs = 0

    for i in range(len(DOI)):
        RefFound = False
        for recordedRef in DatabaseRefs:
            if DOI[i] == recordedRef[1]:
                c.execute('''INSERT INTO PaperReferencesLink(ReferenceID, PaperID) Values (?, ?)''',
                          (recordedRef[0], PaperID))
                RefFound = True

        if not RefFound:
            addedRefs += 1
            c.execute('''INSERT INTO Refs(ReferenceID, DOI, TextRef) Values (?, ?, ?)''',
                      (len(DatabaseRefs) + addedRefs, DOI[i], textRef[i]))
            c.execute('''INSERT INTO PaperReferencesLink(ReferenceID, PaperID) Values (?, ?)''',
                      (len(DatabaseRefs) + addedRefs, PaperID))


def writeToKeywords(c, PaperID, Keywords):
    KeywordList = [item.strip() for item in Keywords.split(",")]
    DatabaseKeywords = c.execute('''SELECT KeywordID, Keyword FROM Keywords''').fetchall()

    addedKeywords = 0
    for Keyword in KeywordList:
        KeywordFound = False
        for recordedKeyword in DatabaseKeywords:
            if Keyword == recordedKeyword[1]:
                c.execute('''INSERT INTO PaperKeywordsLink(PaperID, KeywordID) Values (?, ?)''',
                          (PaperID, recordedKeyword[0]))
                KeywordFound = True

        if not KeywordFound:
            addedKeywords += 1
            c.execute('''INSERT INTO Keywords(KeywordID, Keyword) Values (?, ?)''',
                      (len(DatabaseKeywords) + addedKeywords, Keyword))
            c.execute('''INSERT INTO PaperKeywordsLink(PaperID, KeywordID) Values (?, ?)''',
                      (PaperID, len(DatabaseKeywords) + addedKeywords))

def findEdges(c):
    c.execute('''DELETE FROM Edges''')
    papers = c.execute('''SELECT PaperID, DOI FROM Papers''').fetchall()

    for i in range(len(papers)):
        refs = c.execute('''SELECT ReferenceID FROM PaperReferencesLink WHERE PaperID = ?''', (int(i+1),)).fetchall()

        for j in range(len(refs)):
            ref = c.execute('''SELECT DOI FROM Refs WHERE ReferenceID = ?''', (refs[j][0],)).fetchall()
            for k in range(len(papers)):
                if papers[k][1].lower() == ref[0][0].lower():
                    c.execute('''INSERT INTO Edges(Paper1ID, Paper2ID) Values (?, ?)''', (papers[i][0], papers[k][0]))

def readDatabase():
    conn = sqlite3.connect('Papers.db')
    c = conn.cursor()

    data = {
        'id': [],
        'Title': [],
        'Authors': [],
        'Keywords': [],
        'Summary': [],
        'Link': [],
        'DOI': [],
        'PaperImpact': [],
        'Bibtex': [],
        'Refs': []
    }

    papers = c.execute('''SELECT * FROM Papers''').fetchall()

    for paper in papers:
        data['id'].append(paper[0])
        data['Title'].append(paper[1])
        data['Summary'].append(paper[2])
        data['Link'].append(paper[3])
        data['DOI'].append(paper[4])
        data['PaperImpact'].append(paper[6])
        data['Bibtex'].append(paper[5])

        paperid = paper[0]

        authorids = c.execute('''SELECT AuthorID FROM PaperAuthorsLink WHERE PaperID = ?''', (paperid,)).fetchall()
        authorsList = []
        for authorid in authorids:
            authorsList.append(c.execute('''SELECT * FROM Authors WHERE AuthorID = ?''', authorid).fetchall())

        data['Authors'].append('')
        if len(authorsList) > 4:
            for i in range(3):
                data['Authors'][-1] += authorsList[i][0][1] + ' ' + authorsList[i][0][2]
                data['Authors'][-1] = data['Authors'][-1][:-1]
                data['Authors'][-1] += ', '

            data['Authors'][-1] += 'et al.'

        else:
            for i in range(len(authorsList)):
                data['Authors'][-1] += authorsList[i][0][1] + ' ' + authorsList[i][0][2]
                data['Authors'][-1] = data['Authors'][-1][:-1]
                if i < len(authorsList) - 2:
                    data['Authors'][-1] += ', '
                elif i < len(authorsList) - 1:
                    data['Authors'][-1] += ' and '

        keywordids = c.execute('''SELECT KeywordID FROM PaperKeywordsLink WHERE PaperID = ?''', (paperid,)).fetchall()
        keywordsList = []
        for keywordid in keywordids:
            keywordsList.append(c.execute('''SELECT Keyword FROM Keywords WHERE KeywordID = ?''', keywordid).fetchall()[0][0])

        data['Keywords'].append('')
        for keyword in keywordsList:
            data['Keywords'][-1] += keyword + ', '

        data['Keywords'][-1] = data['Keywords'][-1][:-2]

        referenceids = c.execute('''SELECT ReferenceID FROM PaperReferencesLink WHERE PaperID = ?''', (paperid,)).fetchall()
        referenceList = []
        for referenceid in referenceids:
            referenceList.append(c.execute('''SELECT TextRef FROM Refs WHERE ReferenceID = ?''', referenceid).fetchall()[0][0])

        data['Refs'].append(referenceList)

    edges = c.execute('''SELECT * FROM Edges''').fetchall()

    return data, edges