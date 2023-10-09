import re
from datetime import datetime, date
from random import choice as r_c
import mysql.connector as my
from tabulate import tabulate
from forex_python.converter import CurrencyRates
import time


print("""Connecting to the server...
Secure connection established.\n\n\n\n""")

mydb = my.connect(host='localhost', user='root', passwd='password', autocommit=True)
mycursor = mydb.cursor()
mycursor.execute("Create Database if not exists HackAI")
print("CHECKING AND CREATING DATABASE...")
mycursor.execute("use HackAI")
print("DATABASE CREATED AND CHECKED SUCCESSFULLY.\n\n\n\n\n\n\n")

SEED = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_1234567890#"


# DEFINING FUNCTIONS


def random_id():
    buffer = ""
    for i in range(9):
        buffer += r_c(SEED)
    return buffer

def is_valid_username(username):
    # Username should contain only letters, numbers, underscores, or hyphens
    if re.match(r'^[a-zA-Z0-9_-]+$', username):
        return True
    else:
        print("Invalid username. It should contain only letters, numbers, underscores, or hyphens.")
        return False


def is_valid_password(password):
    # Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit
    if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password):
        return True
    else:
        print("Invalid password. It should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
        return False


def is_valid_email(email):
    # Basic email validation using a simple regular expression
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    else:
        print("Invalid email address. Please enter a valid email address.")
        return False


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


def main():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    email = input("Enter an email address: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")

    if is_valid_username(username) and is_valid_password(password) and is_valid_email(email) and is_valid_dob(dob):
        print("Valid input.")
    else:
        print("Invalid input. Please check your details and try again.")

if __name__ == "__main__":
    main()

def currency_converter():
    c = CurrencyRates()
    
    base_currency = "EUR"  # Fixed base currency
    amount = float(input(f"Enter the amount in {base_currency}: "))

    print("Available foreign currencies:")
    foreign_currencies = input("Enter foreign currencies to convert to (comma-separated, e.g., USD,GBP): ").upper().split(',')

    converted_amounts = {}
    
    for foreign_currency in foreign_currencies:
        foreign_currency = foreign_currency.strip()
        if foreign_currency in c.get_rates(base_currency):
            converted_amount = c.convert(base_currency, foreign_currency, amount)
            converted_amounts[foreign_currency] = converted_amount
        else:
            print(f"Skipping invalid currency: {foreign_currency}")

    if converted_amounts:
        print(f"{amount} {base_currency} is equal to:")
        for foreign_currency, converted_amount in converted_amounts.items():
            print(f"{converted_amount:.2f} {foreign_currency}")
    else:
        print("No valid foreign currencies provided.")

if __name__ == "__main__":
    currency_converter()



def set_currency_thresholds():
    c = CurrencyRates()

    # Get the list of available foreign currencies
    base_currency = "EUR"  # Fixed base currency
    available_currencies = list(c.get_rates(base_currency).keys())

    # Initialize a dictionary to store currency thresholds
    currency_thresholds = {}

    # Allow the user to input thresholds for multiple foreign currencies
    print("Available foreign currencies:")
    for i, currency in enumerate(available_currencies):
        print(f"{i + 1}. {currency}")
    
    while True:
        try:
            currency_index = int(input("Enter the number corresponding to the currency (0 to finish): "))
            if currency_index == 0:
                break
            if currency_index < 1 or currency_index > len(available_currencies):
                print("Invalid choice. Please enter a valid number.")
                continue
            currency = available_currencies[currency_index - 1]
            threshold = float(input(f"Enter the threshold value for {currency}: "))
            currency_thresholds[currency] = threshold
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Poll exchange rates and send alerts
    while True:
        for currency, threshold in currency_thresholds.items():
            current_rate = c.get_rate(base_currency, currency)
            print(f"Current exchange rate for {currency}: {current_rate:.2f}")
            if current_rate > threshold:
                print(f"ALERT: Exchange rate for {currency} has surpassed the threshold of {threshold}")
        time.sleep(60)  # Poll every minute

if __name__ == "__main__":
    set_currency_thresholds()

'''This code defines three functions (is_valid_username, is_valid_password, and is_valid_email) to 
check the validity of the username, password, and email using regular expressions. 
The main function takes user input for these three fields and checks their validity. 
If all fields are valid, it prints "Valid input." Otherwise, it prints "Invalid input."'''







# def is_valid_gender(gender):
#     accepted_genders = ['male', 'female', 'others']
#     return gender in accepted_genders


# def get_gender():
#     while True:
#         gender = input('Enter the gender (Male,Female,Others)  :  ').lower()
#         if is_valid_gender(gender):
#             return gender
#         else:
#             print('The Gender Is Not Valid.')



#----------------------------------------------------------i checked till here as of now ------------------------------

def del_user(pid):
    query = f"select * from user where id  = '{pid}'"
    mycursor.execute(query)
    myrecords = mycursor.fetchall()
    if mycursor.rowcount != 0:
        query = f"delete from admit_patients where id = '{pid}'"
        mycursor.execute(query)
        print("The Status of the patient has been updated from admitted to discharged.")
    else:
        print("Error! No patient was found")

def remove_staff():
    id = input("Enter The ID Of The Staff To Be Removed :  ")
    query = f"delete from hospital_staff where id  = '{id}'"
    mycursor.execute(query)
    print("Removed Successfully or the Staff was Not Found")


# creating table


def create_hospital_staff():
    try:
        query = """create table if not exists Hospital_Staff ( ID varchar(20) not null,SNAME varchar(30),
JOB varchar(20),DEPARTMENT varchar(20),SALARY decimal,COMM decimal,
HIREDATE date)"""
        mycursor.execute(query)
    except Exception as e:
        print(e)


def create_admit_patients():
    try:
        query = ''' create table if not exists ADMIT_PATIENTS (ID varchar(10) not null,
PNAME varchar(20) not null, PAGE integer, PGENDER varchar(10), PWEIGHT decimal, PDOA date, ILLNESS varchar(30),
CONSULTANT_DR varchar(30), DIAGNOSIS varchar(30), ADMN_FEE decimal)'''
        mycursor.execute(query)
    except Exception as e:
        print(e)


def create_discharge():
    try:
        query = ''' create table if not exists DISCHARGE_PATIENTS (ID varchar(10) not null,
PNAME varchar(20) not null, P_AGE integer, PGENDER varchar(10), REASON varchar(50), ILLNESS varchar(30), 
DIAGNOSIS varchar(20),COND varchar(20), CONSULTANT_DR varchar(30), PDOA date, PDOD date)'''
        mycursor.execute(query)
    except Exception as e:
        print(e)


# inserting rows


def insert_staff():
    while True:
        sid = random_id()
        name = get_staff_name()
        job = input('Enter the job  :  ').upper()
        dept = input('Enter The Name Of The Department :  ').upper()
        sal = float(input('Enter The Salary Per Month : '))
        comm = float(input('Enter The Commission Per Month :  '))
        hiredate = get_hiredate()
        query = f"""insert into hospital_staff values('{sid}','{name}','{job}','{dept}',{sal},{comm},'{hiredate}')"""
        mycursor.execute(query)
        ans = input('WANNA ENTER MORE VALUES(y/n)  : ')
        if ans.lower() == 'n':
            break


def admit():
    try:
        while True:
            pid = random_id()
            name = get_patient_name()
            weight = float(input('Enter The Weight(in Kg) Of The Patient  :  '))
            age = int(input('Enter The Age Of The Patient  :  '))
            gender = get_gender()
            pdoa = get_admn_date()
            ill = input('Enter The Illnes  :  ')
            cons = input('Enter The Name Of The Consultant Doctor :   ')
            dia = input('Enter The Diagnose Done  :  ')
            amo = float(input('Enter The Total Amount For Admission : '))
            query = f"""insert into ADMIT_PATIENTS values ('{pid}','{name}',{age},'{gender}',{weight},'{pdoa}','{ill}',
            '{cons}','{dia}',{amo})"""
            mycursor.execute(query)
            ans = input('Want To Enter More? (Y/N) :  ')
            if ans in 'Nn':
                print('Patient Was Added Successfully!')
                break
    except Exception as e:
        print(e)

    # displaying contents of the table



def display_staff():
    try:
        mycursor.execute("select * from hospital_staff")
        myrecords = mycursor.fetchall()
        if mycursor.rowcount != 0:
            print(tabulate(myrecords, headers = ['id', 'name',  'job', 'department', 'salary','comm','hiredate'] , tablefmt = 'fancy_grid' ))
        else:
            print('Add staff to see them!')
    except Exception as e:
        print(e)


def search_staff():
    try:
        sid = input('Enter The Staff ID  :  ')
        query = f"select * from hospital_staff where ID = '{sid}'"
        mycursor.execute(query)
        myrecords = mycursor.fetchall()
        if mycursor.rowcount != 0:
            print(tabulate(myrecords, headers = ['id', 'name',  'job', 'department', 'salary','comm','hiredate'] , tablefmt = 'fancy_grid' ))
        else:
            print('No Staff With Such ID Found! Check the ID and Try Again!')
    except Exception as E:
        print("Add staff to see them!")


def search_patients():
    pid = input("Enter The Patient's ID  :  ")
    query = f"select * from admit_patients where ID = '{pid}'"
    mycursor.execute(query)
    myrecords = mycursor.fetchall()
    if mycursor.rowcount != 0:
        print(tabulate(myrecords, headers = ['ID', 'PNAME',  'P_AGE', 'PGENDER', 'PWEIGHT','PDOA','ILLNESS','CONSULTANT_DR','DIAGNOSIS','ADMN_FEE'] , tablefmt = 'fancy_grid' ))
    else:
        print('No Patient With Such ID Found! Check the ID and Try Again!')


def display_patients():
    try:
        mycursor.execute("select * from admit_patients")
        myrecords = mycursor.fetchall()
        c = mycursor.rowcount
        if c == 0:
            print('No Patient has been Admitted Yet')
        else:
            print(tabulate(myrecords, headers = ['ID', 'PNAME',  'P_AGE', 'PGENDER', 'PWEIGHT','PDOA','ILLNESS','CONSULTANT_DR','DIAGNOSIS','ADMN_FEE'] , tablefmt = 'fancy_grid' ))
    except Exception as e:
        print(e)


def display_discharged():
    try:
        query = "select * from discharge_patients"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            print("Nothing to see here!\n No records were found")
        else:
            myrecords = mycursor.fetchall()
            print(tabulate(myrecords, headers = ['ID', 'PNAME',  'P_AGE', 'PGENDER', 'REASON','ILLNESS','DIAGNOSIS','COND','CONSULTANT_DR','P_DOA','P_DOD'] , tablefmt = 'fancy_grid' ))
    except Exception as e:
        print(e)


# Menu Driven


def choice1():
    try:
        while True:
            b = int(input("""\n\n
  +----------+------------------------+  
  |  Press   |          For           |
  +----------+------------------------+
  |    1     |       All staff info   |
  |    2     |       Add new staff    |
  |    3     |       Remove a staff   |
  |    4     |       search staff     |
  |    5     |       Exit             |
  +----------+------------------------+
    Your Choice   :  """))
            if b == 1:
                display_staff()
            elif b == 2:
                create_hospital_staff()
                insert_staff()
                display_staff()
            elif b == 3:
                remove_staff()
                display_staff()
            elif b == 4:
                search_staff()
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


def choice2():
    try:
        while True:
            c = int(input('''\n\n
    +--------+---------------------------------------+        
    | Press  |               For                     |
    +--------+---------------------------------------+        
    |  1     |       All Patient's Info              |
    |  2     |       Admit A Patient                 |
    |  3     |       Discharge A Patients            |
    |  4     |       Search A Patients               |
    |  5     |       Display Discharged Patients     |
    |  6     |       Exit To Main Menu               |
    +--------+---------------------------------------+
      Enter Your Choice  :   '''))
            if c == 1:
                create_admit_patients()
                display_patients()
            elif c == 2:
                create_admit_patients()
                admit()
                display_patients()
            elif c == 3:
                create_discharge()
                discharge()
                display_patients()
            elif c == 4:
                search_patients()
            elif c == 5:
                display_discharged()
            elif c == 6:
                s = input("Are you sure you want to Exit to MAIN MENU? (y/n)  :  ").lower()
                if s in 'y':
                    print("SAVING AND EXITING")
                    break
                elif s not in 'yn':
                    print("Write y/n")
            elif c not in [1, 2, 3, 4, 5, 6]:
                print('Invalid Choice. \nCheck Your Response! ')
    except ValueError as e:
        print(e, "\n Please enter a Valid 'Number' from above.")


print('*****************************************************************************************************')
print('*                                                                                                   *')
print('*                                                                                                   *')
print('*                                  RED CROSS HOSPITAL                                               *')
print('*         (A group of multi-speciality hospital and research centre owned by A&A co.)               *')
print('*                                                                                                   *')
print('*                                                                                                   *')
print('*****************************************************************************************************')
print('\n\n\n')

while True:
    try:
        print('''                          WELCOME TO HOSPITAL MANAGEMENT SYSTEM ''')
        a = int(input('''
   +--------+-------------------+
   | Press  |        For        |
   +--------+-------------------+
   | 1      |     Staff Info    | 
   | 2      |     Patient Info  |
   | 3      |     Exit          |
   +----------------------------+
    Your choice  :  '''))

        if a == 1:
            choice1()
        elif a == 2:
            choice2()
        elif a == 3:
            s = input("Are you sure you want to Exit? (y/n)  :  ").lower()
            if s in 'y':
                print("SAVING AND EXITING")
                break
            elif s not in 'yn':
                print("Write y/n")
        elif a not in [1, 2, 3]:
            print('Invalid Choice. Select a valid option!\n\n')
    except ValueError as e:
        print(e)