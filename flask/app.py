import psycopg2
from datetime import datetime
from flask import Flask, Response, url_for, redirect, render_template, request, session, flash, jsonify
from psycopg2 import extras

app = Flask(__name__)

def create_db_connection():
	role = open('../role.txt').readline().strip()
	connection = psycopg2.connect(
		user=role,
		password="root",
		host="localhost",
		port="1323",
		database="dbsms"
	)
	return connection

@app.route('/')
def startPage():
    return 'Finally Works'
    #return render_template('loadpage.html')     # ASSUMED VARIABLE NAMES

@app.route('/login', methods=['POST', 'GET'])
def checkCredentials():
    if request.method == 'POST':
        username = request.form['username']     # ASSUMED VARIABLE NAMES
        password = request.form['password']     # ASSUMED VARIABLE NAMES

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Retrieve the user's information based on the provided username
            cursor.execute("SELECT username, password FROM Usr WHERE username = %s", (username,))
            user = cursor.fetchone()

            errors = {'username': True, 'password': True}

            # Check if the user exists and the password is correct
            if user:
                errors['username'] = False  # Username is valid

                if user[1] == password:  # Note: Index 1 corresponds to the password field in the tuple
                    errors['password'] = False  # Password is valid

            # Handle the result as needed
            if not any(errors.values()):
                session['username'] = username
                return redirect(url_for('home'))   # ASSUMED VARIABLE NAMES
            else:
                flash('Invalid username or password', 'error')

        except psycopg2.Error as e:
            print("Error checking credentials:", e)
            flash('Error checking credentials', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/createUser', methods=['POST', 'GET'])
def createUser():
    if request.method == 'POST':
        #request information from form(user input)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        display_name = request.form['display_name']
        pfp_filepath = request.form['pfp_filepath']
        birthday = request.form['birthday']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Insert the new user into the database
            cursor.execute("INSERT INTO Usr (username, password, email, display_name, profile_picture, birthday) "
                           "VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, password, email, display_name, pfp_filepath, birthday))
            connection.commit()

            flash('User created successfully', 'success')

        except psycopg2.Error as e:
            print("Error creating user:", e)
            flash('Error creating user', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/editPassword', methods=['POST', 'GET'])
def editPassword():
    if request.method == 'POST':
        #request information from form(user input)
        username = session.get('username')
        new_password = request.form['new_password']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Update the user's password
            cursor.execute("UPDATE Usr SET password = %s WHERE username = %s", (new_password, username))
            connection.commit()

            flash('Password updated successfully', 'success')

        except psycopg2.Error as e:
            print("Error updating password:", e)
            flash('Error updating password', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/editEmail', methods=['POST', 'GET'])
def editEmail():
    if request.method == 'POST':
        #request information from form(user input)
        username = session.get('username')
        new_email = request.form['new_email']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Update the user's email
            cursor.execute("UPDATE Usr SET email = %s WHERE username = %s", (new_email, username))
            connection.commit()

            flash('Email updated successfully', 'success')

        except psycopg2.Error as e:
            print("Error updating email:", e)
            flash('Error updating email', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/editDisplayName', methods=['POST', 'GET'])
def editDisplayName():
    if request.method == 'POST':
        #request information from form(user input)
        username = session.get('username')
        new_display_name = request.form['new_display_name']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Update the user's display name
            cursor.execute("UPDATE Usr SET display_name = %s WHERE username = %s", (new_display_name, username))
            connection.commit()

            flash('Display Name updated successfully', 'success')

        except psycopg2.Error as e:
            print("Error updating display name:", e)
            flash('Error updating display name', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/editPfp', methods=['POST', 'GET'])
def editPfp():
    if request.method == 'POST':
        #request information from form(user input)
        username = session.get('username')
        new_pfp_file_path = request.form['new_pfp_file_path']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Update the user's profile picture
            cursor.execute("UPDATE Usr SET profile_picture = %s WHERE username = %s", (new_pfp_file_path, username))
            connection.commit()

            flash('Profile Picture updated successfully', 'success')

        except psycopg2.Error as e:
            print("Error updating profile picture:", e)
            flash('Error updating profile picture', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/deleteAccount', methods=['POST', 'GET'])
def deleteAccount():
    if request.method == 'POST':
        #request information from form(user input)
        username = session.get('username')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Delete the user's account
            cursor.execute("DELETE FROM Usr WHERE username = %s", (username))
            connection.commit()

            flash('Account Deletion was successful', 'success')

        except psycopg2.Error as e:
            print("Error deleting account:", e)
            flash('Error deleting account', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/followUser', methods=['POST', 'GET'])
def followUser():
    if request.method == 'POST':
        #request information from form(user input)
        follower_user = session.get('username')
        following_user = request.form['following_user']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Update the follow table to add follow tuple
            cursor.execute("INSERT INTO Follow VALUES (%s, %s)", (follower_user, following_user))
            connection.commit()

            flash('Follow was successful', 'success')

        except psycopg2.Error as e:
            print("Error following user:", e)
            flash('Error following user', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/unfollowUser', methods=['POST', 'GET'])
def unfollowUser():
    if request.method == 'POST':
        #request information from form(user input)
        unfollower_user = session.get('username')
        unfollowing_user = request.form['unfollowing_user']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Update follow table to remove follow tuplle
            cursor.execute("DELETE FROM Follow follower_username = %s AND following_username = %s", 
                           (unfollower_user, unfollowing_user))
            connection.commit()

            flash('Unfollow was successful', 'success')

        except psycopg2.Error as e:
            print("Error unfollowing user:", e)
            flash('Error unfollowing user', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/lookUpUser/<string:username>', methods=['POST', 'GET'])
def lookUpUser(username):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Update follow table to remove follow tuplle
        cursor.execute("""
            SELECT username, password, account_creation_date, email, display_name,
                    profile_picture, birthday
            FROM Usr
            WHERE username = %s""", 
            (username,))

        user_details = cursor.fetchone()

        if user_details:
            username, password, creation_date, email, display_name, profile_picture, birthday = user_details
            result = {
                'username': username,
                'password': password,
                'account_creation_date': str(creation_date),
                'email': email,
                'display_name': display_name,
                'profile_picture': profile_picture,
                'birthday': str(birthday)
            }
            return jsonify(result)
        else:
            return None  # User not found


    except psycopg2.Error as e:
        print("Error looking up user:", e)
        flash('User does not exist', 'error')

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('start_page'))

@app.route('/createTweet', methods=['POST', 'GET'])
def createTweet():
    if request.method == 'POST':
        #request information from form(user input)
        username = session.get('username')
        content = request.form['content']
        likes = 0
        reshares = 0

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Get the maximum tweet_id for the user
            cursor.execute("SELECT MAX(tweet_id) FROM Tweet WHERE username = %s", (username,))
            max_tweet_id = cursor.fetchone()[0]

            # Increment tweet_id by 1
            if max_tweet_id is not None:
                tweet_id = max_tweet_id + 1
            else:
                tweet_id = 0  # if the user has no previous tweets

            # Get current timestamp
            timestamp = datetime.now()

            # Insert the new user into the database
            cursor.execute("INSERT INTO Tweet VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, tweet_id, content, likes, reshares, timestamp))
            connection.commit()

            flash('User created successfully', 'success')

        except psycopg2.Error as e:
            print("Error creating tweet:", e)
            flash('Error creating tweet', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/deleteTweet/<int:tweet_id>', methods=['POST', 'GET'])
def deleteTweet(tweet_id):
    if request.method == 'POST':
        username = session.get('username')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Check if the tweet belongs to the logged-in user
            cursor.execute("SELECT username FROM Tweet WHERE tweet_id = %s", (tweet_id,))
            tweet_owner = cursor.fetchone()

            if tweet_owner and tweet_owner[0] == username:
                # Delete the tweet
                cursor.execute("DELETE FROM Tweet WHERE tweet_id = %s", (tweet_id,))
                connection.commit()

                flash('Tweet deleted successfully', 'success')
            else:
                flash('Unauthorized to delete this tweet', 'error')

        except psycopg2.Error as e:
            print("Error deleting tweet:", e)
            flash('Error deleting tweet', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

if __name__ == '__main__':
    app.run()
