import psycopg2
import re
from datetime import date
from models.User import User
from models.Tweet import Tweet
from models.Comment import Comment

current_user = "username1" # Global variable to store the current user

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
        # Retrieve all tuples from the Usr table
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

def print_all_follows():
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Retrieve all tuples from the Follow table
        cursor.execute("SELECT * FROM Follow")
        users = cursor.fetchall()

        # Print each tuple
        for user in users:
            print(user)

    except psycopg2.Error as e:
        print("Error retrieving follows:", e)

    finally:
        connection.commit()
        cursor.close()
        connection.close()

#TODO: add a global variable that stores the current user
#login function that checks if username and password matches database tuple
def checkCredentials(username: str, password: str):
    global current_user  # Reference the global variable
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Retrieve the user's information based on the provided username
        cursor.execute("SELECT username, password FROM Usr WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Check if the user exists and the password is correct
        if user and user[1] == password:  # Note: Index 1 corresponds to the password field in the tuple
            # Set the current_user global variable after successful login
            current_user = username
            return True  # Credentials match an existing user

    except psycopg2.Error as e:
        print("Error checking credentials:", e)

    finally:
        cursor.close()
        connection.close()

    return False  # Credentials do not match an existing user

#Helper function that checks if email address is in correct form
def is_valid_email(email: str):
    # Define a regular expression pattern for a basic email format
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Use re.match to check if the email matches the pattern
    return re.match(email_pattern, email) is not None

#NOTE: TO call create user with birthday in the form: birthday = date(1999, 1, 1)
#function that creates a new user
def createUser(username: str, password: str, email: str, display_name: str, profile_picture: str, birthday: str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Type and format checks
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

#function that edits the current users password
def editPassword(new_password: str):
    global current_user
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Update the user's password
        cursor.execute("UPDATE Usr SET password = %s WHERE username = %s", (new_password, current_user))
        connection.commit()

        print('Password updated successfully')
        return True

    except psycopg2.Error as e:
        print("Error updating password:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()

#function that edits the current users email
def editEmail(new_email: str):
    global current_user
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        if not is_valid_email(new_email):
            return False
        
        # Update the user's email
        cursor.execute("UPDATE Usr SET email = %s WHERE username = %s", (new_email, current_user))
        connection.commit()

        print('Email updated successfully')
        return True

    except psycopg2.Error as e:
        print("Error updating email:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()

#function that edits the current users display name
def editDisplayName(new_display_name: str):
    global current_user
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Update the user's display name
        cursor.execute("UPDATE Usr SET display_name = %s WHERE username = %s", (new_display_name, current_user))
        connection.commit()

        print('Display Name updated successfully')
        return True

    except psycopg2.Error as e:
        print("Error updating display name:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()

#function that edits the current users pfp
def editPfp(new_pfp_file_path: str):
    global current_user
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        if not (new_pfp_file_path.endswith('.png') or new_pfp_file_path.endswith('.jpg')):
            return False
        
        # Update the user's profile picture
        cursor.execute("UPDATE Usr SET profile_picture = %s WHERE username = %s", (new_pfp_file_path, current_user))
        connection.commit()

        print('Profile Picture updated successfully')
        return True

    except psycopg2.Error as e:
        print("Error updating profile picture:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()

#TODO: add a confirmation message before calling delete Account
#TODO: after deleting account, redirect to login page
#function that deletes the current users account
def deleteAccount():
    global current_user
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Delete user account
        cursor.execute("DELETE FROM Usr WHERE username = %s", (current_user, ))
        connection.commit()

        print('Account Deletion was successful')
        return True

    except psycopg2.Error as e:
        print("Failed to delete account:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()

# function that allows user 1 to follow user 2
def followUser(following_user: str):
    global current_user
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Update the follow table to add a follow tuple
        cursor.execute("INSERT INTO Follow VALUES (%s, %s)", (current_user, following_user))
        connection.commit()

        print('Follow was successful')
        return True

    except psycopg2.Error as e:
        print("Error following user:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()

# function that allows user 1 to unfollows user 2
def unfollow_user(unfollowing_user: str):
    global current_user
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Update the follow table to remove a follow tuple
        cursor.execute("DELETE FROM Follow WHERE follower_username = %s AND following_username = %s", 
                       (current_user, unfollowing_user))
        connection.commit()

        print('Unfollow was successful')
        return True

    except psycopg2.Error as e:
        print("Error unfollowing user:", e)
        return False

    finally:
        connection.commit()
        cursor.close()
        connection.close()