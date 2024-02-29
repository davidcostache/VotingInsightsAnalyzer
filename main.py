import sqlite3
import pandas as pd


def main():
    # Create and connect to an SQLite database in memory
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create the Persons and Votes tables
    cursor.execute('''
    CREATE TABLE persons (
        ID VARCHAR(20) PRIMARY KEY,
        Status VARCHAR(10),
        First_Name VARCHAR(50),
        Last_Name VARCHAR(50),
        Email_Address VARCHAR(100),
        Locatie VARCHAR(50)
    );
    ''')

    cursor.execute('''
    CREATE TABLE Votes (
        ID INT PRIMARY KEY,
        voting_date DATETIME,
        chosen_person VARCHAR(20),
        voter INT,
        message VARCHAR(100),
        valid BIT,
        quality VARCHAR(20)
    );
    ''')

    # Insert data into the tables
    persons_data = [
        ('00108901', 'Active', 'Person', 'One', 'person.one@gfk.com', 'Germany'),
        ('00108941', 'Active', 'Person', 'Two', 'person.two@gfk.com', 'France'),
        ('00199990', 'Inactive', 'Person', 'Three', 'person.three@gfk.com', 'Brazil'),
        ('01100003', 'Active', 'Person', 'Four', 'person.four@gfk.com', 'Hong Kong'),
        ('03400110', 'Active', 'Person', 'Five', 'person.five@gfk.com', 'Germany'),
        ('03400360', 'Active', 'Person', 'Six', 'person.six@gfk.com', 'France'),
        ('03402059', 'Inactive', 'Person', 'Seven', 'person.seven@gfk.com', 'Brazil'),
        ('03400565', 'Active', 'Person', 'Eight', 'person.eight@gfk.com', 'Hong Kong'),
        ('03400436', 'Active', 'Person', 'Nine', 'person.nine@gfk.com', 'Hong Kong')
    ]

    votes_data = [
        (253, '2022-10-29 11:54:15', '03400110', 1, 'Vote 1', 1, 'entrepreneur'),
        (254, '2022-10-29 11:55:22', '03400360', 1, 'Vote 2', 0, 'entrepreneur'),
        (255, '2022-10-29 11:56:53', '03402059', 1, 'Vote 3', 1, 'partner'),
        (256, '2022-10-29 11:58:23', '03400565', 1, 'Vote 4', 1, 'developer'),
        (257, '2022-10-29 12:13:00', '03400436', 1, 'Vote 5', 1, 'developer')
    ]

    cursor.executemany('INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?);', persons_data)
    cursor.executemany('INSERT INTO Votes VALUES (?, ?, ?, ?, ?, ?, ?);', votes_data)

    # Generate and display Report 1 using pandas for better formatting
    query1 = '''
    SELECT p.Locatie, p.First_Name || ' ' || p.Last_Name AS Nume, COUNT(v.ID) AS Numar_Voturi, GROUP_CONCAT(v.quality, '; ') AS Calitati
    FROM persons p
    JOIN Votes v ON p.ID = v.chosen_person
    WHERE v.valid = 1
    GROUP BY p.Locatie, p.First_Name, p.Last_Name
    ORDER BY p.Locatie, Numar_Voturi DESC;
    '''
    cursor.execute(query1)
    df1 = pd.DataFrame(cursor.fetchall(), columns=['Location', 'Name', 'Number of Votes', 'Qualities'])
    print("Report 1: Votes and qualities received for each person in each location")
    print(df1)

    # Generate and display Report 2 using pandas for better formatting
    query2 = '''
    SELECT p.Locatie AS Tara, COALESCE(SUM(CASE WHEN v.valid = 1 THEN 1 ELSE 0 END), 0) AS Numar_Voturi
    FROM persons p
    LEFT JOIN Votes v ON p.ID = v.chosen_person
    GROUP BY Tara
    ORDER BY Tara;
    '''
    cursor.execute(query2)
    df2 = pd.DataFrame(cursor.fetchall(), columns=['Country', 'Number of Votes'])
    print("\nReport 2: Votes per country, including 0 for countries without votes")
    print(df2)

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    main()
