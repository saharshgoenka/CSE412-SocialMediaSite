import psycopg2
import re
from datetime import date
from models.User import User
from models.Tweet import Tweet
from models.Comment import Comment

def create_db_connection():
	connection = psycopg2.connect(
        user='enigma',
		host="/tmp",
		port="1322",
		database="enigma"
	)
	return connection

def print_all_users():
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Retrieve all tuples from the Usr tablea
        cursor.execute("SELECT * FROM Usr")
        users = cursor.fetchall()

        # Print each tuple
        for user in users:
            print(user)

    except psycopg2.Error as e:
        print("Error retrieving users:", e)

    finally:
        connection.commit()
        cursor.close()
        connection.close()

#login function that checks if username and password matches database tuple
def check_credentials(username, password):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Retrieve the user's information based on the provided username
        cursor.execute("SELECT username, password FROM Usr WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Check if the user exists and the password is correct
        if user and user[1] == password:  # Note: Index 1 corresponds to the password field in the tuple
            return True  # Credentials match an existing user

    except psycopg2.Error as e:
        print("Error checking credentials:", e)

    finally:
        cursor.close()
        connection.close()

    return False  # Credentials do not match an existing user

#Helper function that checks if email address is in correct form
def is_valid_email(email):
    # Define a regular expression pattern for a basic email format
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Use re.match to check if the email matches the pattern
    return re.match(email_pattern, email) is not None

#function that creates a new user
#REMEMBER TO call create user with birthday in the form: birthday = date(1999, 1, 1)
def create_user(username, password, email, display_name, profile_picture, birthday):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Type and format checks
        if not all(isinstance(arg, str) for arg in [username, password, email, display_name, profile_picture]):
            raise ValueError("Invalid input types")

        if not is_valid_email(email):
            raise ValueError("Invalid email format")

        if not (profile_picture.endswith('.png') or profile_picture.endswith('.jpg')):
            raise ValueError("Invalid profile picture format")
        
        if not isinstance(birthday, date):
            raise ValueError("Invalid birthday format")

        # Get the current date for account creation
        account_creation_date = date.today()

        # Insert the new user into the database
        cursor.execute("INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (username, password, account_creation_date, email, display_name, profile_picture, birthday))
        connection.commit()

    except psycopg2.IntegrityError as e:
        connection.rollback()  # Rollback the transaction
        print("Error creating user:", e)
        return False

    except (psycopg2.Error, ValueError) as e:
        print("Error creating user:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()

    return True