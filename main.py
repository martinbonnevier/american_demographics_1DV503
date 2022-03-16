import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np
import keyboard
import os
import PySimpleGUI as sg
import colorama
from colorama import Fore
from pyfiglet import figlet_format
import sys

# connection to db - creates a connection to the database in MySQL workbench
dbConnection = mysql.connector.connect(user='root',
                                       password='root',
                                       host='localhost',)

# Names database
DB_NAME = 'american_demographics'

# Creates a cursor, acting within MySQL. Is an object, that can hold data as well.
cursor = dbConnection.cursor(buffered=True)

# Reads data from planets.csv file (not provided, must be put in root)
election_data = pd.read_csv('election.csv', index_col=False, delimiter=';')

# Ignores first row in csv file (names of columns)
election_data.head()

# Substitutes NaN with None
election_data = election_data.replace(np.nan, None)

# print(election_data)
# Reads data from demographics.csv file (not provided, must be put in root)
demographics_state_data = pd.read_csv('demographics.csv', index_col=False, delimiter=';')
demographics_state_data.head()

# Substitute NaN with None
demographics_state_data = demographics_state_data.replace(np.nan, None)

# # Reads data from education.csv file (not provided, must be put in root)
relation_data = pd.read_csv('state_election.csv', index_col=False, delimiter=';')
relation_data.head()

# Substitute NaN with None
relation_data = relation_data.replace(np.nan, None)

# Creates database


def createDatabase(cursor, DB_NAME):

    try:
        cursor.execute(
            "DROP DATABASE IF EXISTS american_demographics")
    except mysql.connector.Error as err:
        print("Failed to drop database {}".format(err))
        exit(1)



    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed to create database {}".format(err))
        exit(1)


def closeDatabaseConnection():
    cursor.close()
    dbConnection.close()


def populateTables(cursor):
    try:
        # checks if database is connected
        if dbConnection.is_connected():
            dbConnection.database = DB_NAME
            print("You're connected to database:", dbConnection.database)
            cursor.execute('DROP TABLE IF EXISTS election;')
            cursor.execute('DROP TABLE IF EXISTS demographics;')
            cursor.execute('DROP TABLE IF EXISTS relation;')

            # creates a table and populates it with data
            cursor.execute(
                "CREATE TABLE election(id int(11),year int(11),state varchar(255),office varchar(255),candidate varchar(255),candidatevotes int(11),totalvotes int(11),party_simplified varchar(255),PRIMARY KEY(id))")
            print("Table is being created....")
            for i, row in election_data.iterrows():
                electionValues = "INSERT INTO election(id,year,state,office,candidate,candidatevotes,totalvotes,party_simplified) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(electionValues, tuple(row))
                # Kept in case one needs to see data being insterted into table
                # print(str(i) + ": Data inserted into table 'election'")

            # creates a table and populates it with data
            cursor.execute("CREATE TABLE demographics(id int(11),State varchar(255),Population_2014 int(11),Miscellaneous_Foreign_Born int(11),Housing_Households int(11),Housing_Households_with_a_Internet int(11),Education_High_School_or_Higher int(11),Education_Bachelors_Degree_or_Higher int(11),Income_Per_Capita_Income int(11), PRIMARY KEY(id))")
            print("Table is being created....")
            for i, row in demographics_state_data.iterrows():
                # print(row)

                demographicValues = "INSERT INTO demographics(id,State,Population_2014,Miscellaneous_Foreign_Born,Housing_Households,Housing_Households_with_a_Internet,Education_High_School_or_Higher,Education_Bachelors_Degree_or_Higher,Income_Per_Capita_Income) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                cursor.execute(demographicValues, tuple(row))
                # print("demographics")
                # Kept in case one needs to see data being insterted into table
                # print(str(i) + ": Data inserted into table 'demographics'")

             # creates a table and populates it with data
            cursor.execute("CREATE TABLE relation(election_id int(11), state_id int(11), FOREIGN KEY(election_id) REFERENCES election(id), FOREIGN KEY(state_id) REFERENCES demographics(id))")
            print("Table is being created....")
            for i, row in relation_data.iterrows():
                # print(row)

                demographicValues = "INSERT INTO relation (election_id, state_id) VALUES (%s,%s)"

                cursor.execute(demographicValues, tuple(row))

                # Kept in case one needs to see data being insterted into table
                # print(str(i) + ": Data inserted into table 'education'")
            # # adds populated tables to databas
            dbConnection.commit()

    except mysql.connector.Error as err:
        print("Error while connecting to MySQL", err)
# Enum for menu options
optionsEnum = {
    1: 'Show the sum of democrat votes per state for a specifik year',
    2: '(VIEW) show states where more than 80 % of households have an internet connection',
    3: 'Show which candidate won during a given year in states with a chosen percentage of people with a Bachelor degree or higher',
    4: 'Show which candidate and party won during a given year in states, sorted by income per capita',
    5: 'List all States by number of foreign born -> Who got most votes',
    6: 'Exit',
}
# Clears console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

# Print menu options
def printMenu():
    for key in optionsEnum.keys():
        print(key, '--', optionsEnum[key])



def loopMenu():
    while(True):
        clearConsole()
        printMenu()
        option = ''
        try:
            option = int(input('Enter selection: '))
        except:
            print('Wrong input. Please enter a number!')
        # Check what choice was entered and act accordingly
        if option == 1:
            print('1')
            option1()
        elif option == 2:
            print('2')
            option2()
        elif option == 3:
            print('3')
            option3()
        elif option == 4:
            print('4')
            option4()
        elif option == 5:
            print('5')
            option5()
        elif option == 6:
            print('6')
            print('Good Bye!')
            closeDatabaseConnection()
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')

def option1():
  year = input('Enter a year: ')

  query = "SELECT SUM(candidatevotes) as sumOfVotes, state  FROM election WHERE party_simplified = 'DEMOCRAT' AND year = '"+year+"' GROUP BY state;"
  cursor.execute(query)
  
  print(Fore.RED + "| {:<45} | {:<45} |".format("Sum of democrat votes",
          "State"))
  for (sumOfVotes, state) in cursor:
    print(Fore.YELLOW + "| {:<45} | {:<45} |".format(sumOfVotes,state))
  print(Fore.WHITE + 'Press any key to return to menu.')
  a = keyboard.read_key()
  a = keyboard.read_key()

def option2():
  query = "CREATE VIEW households_with_internet_connection AS SELECT State, Housing_Households_with_a_Internet FROM demographics WHERE Housing_Households_with_a_Internet > 80;"
  query2 = "select * from households_with_internet_connection GROUP BY State, Housing_Households_with_a_Internet DESC;"
  cursor.execute(query)
  cursor.execute(query2)


  print(Fore.RED + "| {:<45} | {:<45} |".format("State",
          "Percent of households with internet"))
  for (State, Housing_Households_with_a_Internet) in cursor:
    print(Fore.YELLOW + "| {:<45} | {:<45} |".format(State,Housing_Households_with_a_Internet))
  print(Fore.WHITE + 'Press any key to return to menu.')
  a = keyboard.read_key()
  a = keyboard.read_key()

def option3():
  year = input("Please specify year: ")
  bachelor = input("Please specify % of people with a Bachelor degree or higher: ") 
  query = "select demographics.state as state, filtered_election.candidate as candidate, filtered_election.max_candidatevotes as candidatevotes, filtered_election.party_simplified as party, demographics.Education_Bachelors_Degree_or_Higher as bachelordegree from demographics join relation on demographics.id = state_id join (select id, candidate, party_simplified, max(election.candidatevotes) as max_candidatevotes from election where election.year='"+year+"' group by election.State) as filtered_election on filtered_election.id = election_id where demographics.Education_Bachelors_Degree_or_Higher > "+bachelor+" group by state_id order by demographics.Education_Bachelors_Degree_or_Higher desc"
  cursor.execute(query)
  # for (row) in cursor:
  #   print(row)

  print(Fore.RED + "| {:<20} | {:<20} | {:<20} | {:<20} | {:<20} |".format("State",
          "Candidate", "Candidate Votes", "Political party", "% with Bachelor's degree or higher"))
  for (state, candidate, candidatevotes, party, bachelordegree ) in cursor:
    print(Fore.YELLOW + "| {:<20} | {:<20} | {:<20} | {:<20} | {:<20} |".format(state, candidate, candidatevotes, party, bachelordegree ))
  print(Fore.WHITE + 'Press any key to return to menu.')
  a = keyboard.read_key()
  a = keyboard.read_key()
# Main
def option4():
  
  year = input("Please specify year: ")
  query = "select demographics.state as state, filtered_election.candidate as candidate, filtered_election.max_candidatevotes as candidatevotes, filtered_election.party_simplified as party, demographics.Income_Per_Capita_Income as incomepercapita from demographics join relation on demographics.id = state_id join (select id, candidate, party_simplified, max(election.candidatevotes) as max_candidatevotes from election where election.year='"+year+"' group by election.State) as filtered_election on filtered_election.id = election_id group by state_id order by demographics.Income_Per_Capita_Income desc"
  cursor.execute(query)
  print(Fore.RED + "| {:<20} | {:<20} | {:<20} | {:<20} | {:<20} |".format("State",
          "Candidate", "Candidate Votes", "Political party", "Income per capita (descending)"))
  for (state, candidate, candidatevotes, party, incomepercapita ) in cursor:
    print(Fore.YELLOW + "| {:<20} | {:<20} | {:<20} | {:<20} | {:<20} |".format(state, candidate, candidatevotes, party, incomepercapita ))
  print(Fore.WHITE + 'Press any key to return to menu.')
  a = keyboard.read_key()
  a = keyboard.read_key()

def option5():
    # List all States by number of foreign born -> Who got most votes
  year = input("Please specify year: ")
  query = "select demographics.state as state, filtered_election.candidate as candidate, filtered_election.max_candidatevotes as candidatevotes, filtered_election.party_simplified as party, demographics.Miscellaneous_Foreign_Born as Foreignborn from demographics join relation on demographics.id = state_id join (select id, candidate, party_simplified, max(election.candidatevotes) as max_candidatevotes from election where election.year='"+year+"' group by election.State) as filtered_election on filtered_election.id = election_id group by state_id order by demographics.Miscellaneous_Foreign_Born desc"
  cursor.execute(query)
  print(Fore.RED + "| {:<20} | {:<20} | {:<20} | {:<20} | {:<20} |".format("State",
          "Candidate", "Candidate Votes", "Political party", "% Foreign Born (descending)"))
  for (state, candidate, candidatevotes, party, Foreignborn ) in cursor:
    print(Fore.YELLOW + "| {:<20} | {:<20} | {:<20} | {:<20} | {:<20} |".format(state, candidate, candidatevotes, party, Foreignborn ))
  print(Fore.WHITE + 'Press any key to return to menu.')
  a = keyboard.read_key()
  a = keyboard.read_key()

createDatabase(cursor, DB_NAME)

    # connects database
dbConnection.database = DB_NAME
    # print("Database created successfully.")

# creates tables and populates them with data
populateTables(cursor)
# trialQueries(cursor)

# # loops main menu in while loop that spins until user exists
loopMenu()
