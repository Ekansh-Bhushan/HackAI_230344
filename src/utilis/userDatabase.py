
import re
from datetime import datetime, date
from random import choice as r_c
import mysql.connector as my
from tabulate import tabulate

import time


import smtplib
from email.mime.text import MIMEText
import json
import config
import csv


print("""Connecting to the server...
Secure connection established.\n\n\n\n""")

mydb = my.connect(host='localhost', user='root', passwd=config.MYSQL_PASSWORD, autocommit=True)
mycursor = mydb.cursor()
mycursor.execute("Create Database if not exists HackAI")
print("CHECKING AND CREATING DATABASE...")
mycursor.execute("use HackAI")
print("DATABASE CREATED AND CHECKED SUCCESSFULLY.\n\n\n\n\n\n\n")

SEED = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_1234567890#"



def random_id():
    buffer = ""
    for i in range(9):
        buffer += r_c(SEED)
    return buffer

def is_valid_name(name):
    is_valid = True
    for letter in name:
        if not (letter.isalpha() or letter.isspace()):
            is_valid = False
    return is_valid

def get_user_name():
    while True:
        name = input("Enter The Name : ").title()
        if is_valid_name(name):
            return name
        else:
            print("That Name Isn't Valid, Names Can Only Contain Letters And Spaces. \nTry Again...")

def is_valid_password(password):
    # Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit
    if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password):
        return True
    else:
        return False

def get_user_pasword():
    while True:
        password = input("Enter The Password : ").title()
        if is_valid_password(password):
            return password
        else:
            print("Invalid password. It should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.\nTry Again...")
       

def is_valid_email(email):
    # Basic email validation using a simple regular expression
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    else:
        
        return False

def get_user_email():
    while True:
        email = input("Enter The email : ").title()
        if is_valid_email(email):
            return email
        else:
            print("Invalid email address. Please enter a valid email address.\nTry Again...")

def is_validate_date(date):
    fields = date.split("-")
    contains_all_fields = len(fields) == 3
    all_fields_are_integers = all([field.isdigit() for field in fields])
    return contains_all_fields and all_fields_are_integers

def get_dob():
    while True:
        date = input("Enter The dob (dd-mm-yyyy) : ")
        if is_validate_date(date):
            day, month, year = [int(field) for field in date.split("-")]
            try:
                date = datetime(year, month, day)
                if date > datetime.today():
                    raise ValueError
                return date
            except ValueError:
                print("The Date You Entered Doesn't Exists, Or it is grater than today. Try That Again...")
        else:
            print("Your Answer Might Not Be In The Mentioned Date Format, Try That Again...")

# Opening the CSV file and reading its contents into a dictionary
dicti = {}
with open('C:/Users/Ekansh/code/HackAI/exchange_rates.csv', mode='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        acronym = lines[0].strip()  # Assuming acronyms are in the first column
        full_form = lines[1].strip()  # Assuming full forms are in the second column
        dicti[acronym] = full_form

# checking is currency name enter by the user is valid 
def is_valid_currency_name(currency_name):
    # Check if the currency code is in the dictionary
    return currency_name in dicti

def get_currency_key(currency_name):
    # Return the key (acronym) for a given currency value
    for key, value in dicti.items():
        if value == currency_name:
            return key
    return None

def add_currency_name():
    while True:
        currency_name = input("Enter The currency name CODE (e.g., INR, USD): ").upper()
        if is_valid_currency_name(currency_name):
            return currency_name
        else:
            print("Invalid currency code. Please try again...")

def valid_currency():
    currency_code = add_currency_name()
    if currency_code:
        print(f"You entered a valid currency code: {currency_code}")
    else:
        print("No valid currency code entered.")

def input_threshold_values():
    thresholds = {}  # Dictionary to store threshold values for currencies

    while True:
        currency = input("Enter a currency code (or 'done' to finish): ").upper()
        if currency == 'DONE':
            break

        while True:
            threshold_str = input(f"Enter the threshold value for {currency}: ")
            try:
                threshold = float(threshold_str)
                thresholds[currency] = threshold
                break
            except ValueError:
                print("Invalid input. Please enter a valid numerical threshold.")

    return thresholds


thresholds = input_threshold_values()

print("Threshold values:")
for currency, threshold in thresholds.items():
    print(f"{currency}: {threshold}")



# creating tables 

def create_user_table():
    try:
        query = ''' create table if not exists USER (ID varchar(10) not null,
UNAME varchar(20) not null, EMAIL varchar(200), PASSWORD varchar(50),UDOB date)'''
        mycursor.execute(query)
    except Exception as e:
        print(e)

def add_user():
    try:
        while True:
            pid = random_id()
            name = get_user_name()
            email = get_user_email()
            password = get_user_pasword()
            udob = get_dob()
            query = f"""insert into USER values ('{pid}','{name}','{email}','{password}','{udob}')"""
            mycursor.execute(query)
            ans = input('Want To Enter More? (Y/N) :  ')
            if ans in 'Nn':
                print('User Was Added Successfully!')
                print("User will get notification on email whenever currency rates goes below the threshold value")
                break
    except Exception as e:
        print(e)


def display_user():
    try:
        mycursor.execute("select * from USER")
        myrecords = mycursor.fetchall()
        if mycursor.rowcount != 0:
            print(tabulate(myrecords, headers = ['id', 'name',  'email', 'password', 'udob'] , tablefmt = 'fancy_grid' ))
        else:
            print('Add USER to see them!')
    except Exception as e:
        print(e)

def search_user():
    try:
        sid = input('Enter The User ID  :  ')
        query = f"select * from USER where ID = '{sid}'"
        mycursor.execute(query)
        myrecords = mycursor.fetchall()
        if mycursor.rowcount != 0:
            print(tabulate(myrecords, headers = ['id', 'name',  'email', 'password', 'udob'] , tablefmt = 'fancy_grid' ))
        else:
            print('No User With Such ID Found! Check the ID and Try Again!')
    except Exception as E:
        print("Add User to see them!")

def del_user(pid):
    query = f"select * from USER where id  = '{pid}'"
    mycursor.execute(query)
    myrecords = mycursor.fetchall()
    if mycursor.rowcount != 0:
        query = f"delete from USER where id = '{pid}'"
        mycursor.execute(query)
        print("The user is deleted from database.")
    else:
        print("Error! No USER was found")


def choice():
    try:
        while True:
            b = int(input("""\n\n
  +----------+------------------------+  
  |  Press   |          For           |
  +----------+------------------------+
  |    1     |       All USER info    |
  |    2     |       Add new USER     |
  |    3     |       Remove a USER    |
  |    4     |       search USER      |
  |    5     |       Exit             |
  +----------+------------------------+
    Your Choice   :  """))
            if b == 1:
                display_user()
            elif b == 2:
                create_user_table()
                add_user()
                display_user()
            elif b == 3:
                del_user()
                display_user()
            elif b == 4:
                search_user()
            elif b == 5:
                s = input("Are you sure you want to Exit to MAIN MENU? (y/n)  :  ").lower()
                if s in 'y':
                    print("SAVING AND EXITING")
                    break
                elif s not in 'yn':
                    print("Write y/n")
            else:
                print('Invalid Choice. \nCheck Your Response! ')
    except ValueError as e:
        print(e, "\n Please enter a Valid 'Number' from above.")

def userDatabase():
    print("""
        WELCOME TO CURRENCY EXCHANGE MONITOR & ALERT PLATFORM 
    """)