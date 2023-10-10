from uagents import Agent, Context
import re
from datetime import datetime, date
from random import choice as r_c
import mysql.connector as my
from tabulate import tabulate
from forex_python.converter import CurrencyRates
import time
import requests
import pandas as pd
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