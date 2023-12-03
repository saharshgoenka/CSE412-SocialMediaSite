import psycopg2
from datetime import datetime
from flask import Flask, Response, url_for, redirect, render_template, request, session, flash, jsonify
from psycopg2 import extras

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'your_secret_key_here'


def create_db_connection():
    connection = psycopg2.connect(
        user='postgres',
        host="localhost",
        port=5439,
        database="social_media_data"
    )

    return connection



# root
@app.route('/')
def start_page():
    return render_template('login.html')


@app.route('/test', methods=['GET'])
def test():
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Usr ")
        users = cursor.fetchall()

        formatted_users = {}

        for user in users:
            formatted_users[user[0]] = user

        return jsonify(formatted_users)
    except psycopg2.Error as e:
        print("Error:", e)
        flash('Error', 'error')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT username, password FROM Usr WHERE username = %s", (username,))
            user = cursor.fetchone()

            errors = {'username': True, 'password': True}

            if user:
                errors['username'] = False

                if user[1] == password:
                    errors['password'] = False

            if not any(errors.values()):
                session['username'] = username
                return redirect(url_for('homepage'))  # Change to the new route
            else:
                flash('Invalid username or password', 'error')

        except psycopg2.Error as e:
            print("Error checking credentials:", e)
            flash('Error checking credentials', 'error')

        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')


# Add a new route for the homepage
@app.route('/homepage')
def homepage():
    if 'username' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Select all tweets from the Tweet table
            cursor.execute("SELECT original_username, cntnt, likes, reshares, timestmp FROM Tweet")
            tweets = cursor.fetchall()

            return render_template('homepage.html', username=session['username'], tweets=tweets)

        except psycopg2.Error as e:
            print("Error fetching tweets:", e)
            flash('Error fetching tweets', 'error')

        finally:
            cursor.close()
            connection.close()

    else:
        flash('You must log in first', 'error')
        return redirect(url_for('start_page'))

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/createUser', methods=['POST', 'GET'])
def createUser():
    if request.method == 'POST':
        # request information from form(user input)
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
        # request information from form(user input)
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
        # request information from form(user input)
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
        # request information from form(user input)
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
        # request information from form(user input)
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
        # request information from form(user input)
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
        # request information from form(user input)
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
        # request information from form(user input)
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
        # request information from form(user input)
        username = session.get('username')
        content = request.form['content']
        likes = 0
        reshares = 0

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Get the maximum tweet_id for the user
            cursor.execute("SELECT MAX(tweet_id) FROM Tweet WHERE original_username = %s", (username,))
            max_tweet_id = cursor.fetchone()[0]

            # Increment tweet_id by 1
            if max_tweet_id is not None:
                tweet_id = max_tweet_id + 1
            else:
                tweet_id = 0  # if the user has no previous tweets

            # Get current timestamp
            timestamp = datetime.now()

            # Insert the new tweet into the database
            cursor.execute("INSERT INTO Tweet VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, tweet_id, content, likes, reshares, timestamp))
            connection.commit()

            flash('Tweet created successfully', 'success')

        except psycopg2.Error as e:
            print("Error creating tweet:", e)
            flash('Error creating tweet', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('homepage'))  # Redirect to the updated homepage route


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

# Add a new route for the settings page
@app.route('/settings')
def settings_page():
    if 'username' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Retrieve user details for settings page
            cursor.execute("SELECT * FROM Usr WHERE username = %s", (session['username'],))
            user_details = cursor.fetchone()

            return render_template('settings.html', user_details=user_details)

        except psycopg2.Error as e:
            print("Error fetching user details:", e)
            flash('Error fetching user details', 'error')

        finally:
            cursor.close()
            connection.close()
    else:
        flash('You must log in first', 'error')
        return redirect(url_for('start_page'))


# Add a new route and functions for editing settings
@app.route('/editSettings', methods=['POST'])
def editSettings():
    if request.method == 'POST':
        # Handle the form submission to update user settings
        # Retrieve form data using request.form and update the database

        flash('Settings updated successfully', 'success')

    return redirect(url_for('settings_page'))


if __name__ == '__main__':
    app.run()
