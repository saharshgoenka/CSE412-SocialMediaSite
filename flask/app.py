import os
from datetime import datetime

import psycopg2
from flask import Flask, url_for, redirect, render_template, request, session, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), UPLOAD_FOLDER)

# Ensure the 'uploads' directory exists
uploads_dir = os.path.join(os.getcwd(), UPLOAD_FOLDER)
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)


def create_db_connection():
    connection = psycopg2.connect(
        user='enigma',
        host="/tmp",
        port="1322",
        database="enigma"
    )

    return connection

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # flash('Error', 'error')

@app.route('/loadUserProfile/<string:username>')
def loadUserProfile(username):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Retrieve user details for the profile dropdown
        cursor.execute("SELECT * FROM Usr WHERE username = %s", (username,))
        user_details = cursor.fetchone()

        sql_query = """
        WITH UserTweets AS (
            SELECT *
            FROM tweet
            WHERE original_username = %s
        ),
        UserReshares AS (
            SELECT *
            FROM tweet t
            WHERE (t.original_username, t.tweet_id) IN (
                SELECT r.tweeting_username, r.tweet_id
                FROM reshare r
                WHERE r.resharing_username = %s
            )
        )

        SELECT * FROM UserTweets UNION SELECT * FROM UserReshares;
        """

        cursor.execute(sql_query, (username, username))
        tweet_details = cursor.fetchall()

        cursor.execute("SELECT * FROM Follow WHERE follower_username = %s AND following_username = %s", (session["username"], username))
        follower_details = cursor.fetchall()

        print(len(follower_details))
        if len(follower_details):
            follower_details = {'showButton' : False, 'following_username' : username}
        else:
            follower_details = {'showButton' : True, 'following_username' : username}
        
        print(follower_details)
        return render_template('profile.html', user_details=user_details, tweet_details=tweet_details, follower_details=follower_details)

    except psycopg2.Error as e:
        print("Error fetching user profile data:", e)
        # flash('Error fetching user profile data', 'error')

    finally:
        cursor.close()
        connection.close()

    return render_template('profile.html', user_details=user_details)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT username, password, display_name FROM Usr WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                if user[1] == password:
                    session['displayname'] = user[2]
                    session['username'] = username
                    # flash('Login successful', 'success')
                    return redirect(url_for('homepage'))
                else:
                    flash('Invalid username or password', 'error')
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
            # Retrieve user details for the profile dropdown
            cursor.execute("SELECT * FROM Usr WHERE username = %s", (session['username'],))
            user_details = cursor.fetchone()

            # Select all tweets from the Tweet table and join with the Media table
            cursor.execute("""
                SELECT 
                    T.original_username, 
                    T.tweet_id, 
                    T.cntnt, 
                    T.likes, 
                    T.reshares, 
                    T.timestmp,
                    M.media_url
                FROM Tweet T
                LEFT JOIN Media M ON T.original_username = M.username AND T.tweet_id = M.tweet_id
                ORDER BY T.timestmp DESC
            """)
            tweets = cursor.fetchall()

            return render_template('homepage.html', username=session['username'], user_details=user_details,
                                   tweets=tweets)

        except psycopg2.Error as e:
            print("Error fetching data:", e)
            flash('Error fetching data', 'error')

        finally:
            cursor.close()
            connection.close()

    else:
        flash('You must log in first', 'error')
        return redirect(url_for('start_page'))

def save_media_file(file, username, tweet_id):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Store only the relative path in the database
        media_url = f'uploads/{filename}'

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Insert the media record into the Media table
            cursor.execute("INSERT INTO Media VALUES (%s, %s, %s)",
                           (username, tweet_id, media_url))
            connection.commit()

        except psycopg2.Error as e:
            print("Error saving media file:", e)

        finally:
            cursor.close()
            connection.close()

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

            # Save media file if provided
            if 'media_file' in request.files:
                media_file = request.files['media_file']
                save_media_file(media_file, username, tweet_id)
                print("works!")

            # flash('Tweet created successfully', 'success')

        except psycopg2.Error as e:
            print("Error creating tweet:", e)
            flash('Error creating tweet', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('homepage'))  # Redirect to the updated homepage route


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/tweet_details/<int:tweet_id>/<string:username>')
def tweet_details(tweet_id, username):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Retrieve tweet details
        cursor.execute("SELECT * FROM Tweet WHERE tweet_id = %s AND original_username = %s", (tweet_id, username))
        tweet = cursor.fetchone()

        if tweet:
            # Retrieve comments for the tweet
            cursor.execute("SELECT * FROM Cmmnt WHERE tweet_id = %s AND tweeting_username = %s", (tweet_id, username))
            comments = cursor.fetchall()

            return render_template('tweet_details.html', tweet=tweet, comments=comments)
        else:
            flash('Tweet not found', 'error')
            return redirect(url_for('homepage'))

    except psycopg2.Error as e:
        print("Error fetching tweet details:", e)
        flash('Error fetching tweet details', 'error')

    finally:
        cursor.close()
        connection.close()

@app.route('/addComment/<int:tweet_id>/<string:username>', methods=['POST'])
def addComment(tweet_id, username):
    commenting_username = session.get('username')
    comment_content = request.form['comment']  # Updated this line to get the comment content from the form

    createComment(commenting_username, username, tweet_id, comment_content)

    return redirect(url_for('tweet_details', tweet_id=tweet_id, username=username))

def createComment(commenting_username, tweeting_username, tweet_id, comment_content):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Create current timestamp  and format it
        timestmp_intermediate = datetime.now()
        timestmp = timestmp_intermediate.strftime("%Y-%m-%d %H:%M:%S")

        # Insert the new comment into the DB
        cursor.execute(
            "INSERT INTO Cmmnt(commenting_username, tweeting_username, tweet_id, timestmp, comment_content) VALUES (%s, %s, %s, %s, %s)",
            (commenting_username, tweeting_username, tweet_id, timestmp, comment_content))

    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        # Commit changes
        connection.commit()
        cursor.close()
        connection.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/createUser', methods=['POST', 'GET'])
def createUser():
    if request.method == 'POST':
        # request information from form(user input)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        display_name = request.form['display_name']
        birthday = request.form['birthday']
        acc_creation_date = datetime.now()

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            if 'pfp_file' in request.files:
                pfp_file = request.files['pfp_file']
                if pfp_file and allowed_file(pfp_file.filename):
                    filename = secure_filename(pfp_file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    pfp_file.save(filepath)

                    # Store only the relative path in the database
                    profile_picture_path = f'uploads/{filename}'

                else:
                    # flash('Invalid file format for profile picture. Allowed formats: png, jpg, jpeg, gif', 'error')
                    return redirect(url_for('signup'))

            else:
                # Use a default profile picture if no file is provided
                profile_picture_path = 'default_picture.jpeg'

            # Insert the new user into the database with the profile picture filepath
            cursor.execute("INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (username, password, acc_creation_date, email, display_name, profile_picture_path, birthday))
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

            # flash('Profile Picture updated successfully', 'success')

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
            cursor.execute("DELETE FROM Usr WHERE username = %s", (username,))
            connection.commit()

            # Clear session after deleting the account
            session.pop('username', None)

            flash('Account Deletion was successful', 'success')

        except psycopg2.Error as e:
            print("Error deleting account:", e)
            flash('Error deleting account', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/likeTweet/<int:tweet_id>/<string:username>', methods=['POST'])
def likeTweet(tweet_id, username):

    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Update the like count in the database
        cursor.execute("UPDATE Tweet SET likes = likes + 1 WHERE tweet_id = %s AND original_username = %s",
                       (tweet_id, username))
        connection.commit()
        print("likeTweet: like count updated")

        # Retrieve the updated like count
        cursor.execute("SELECT likes FROM Tweet WHERE tweet_id = %s AND original_username = %s",
                       (tweet_id, username))
        updated_likes = cursor.fetchone()[0]

        return jsonify({'likes': updated_likes})

    except psycopg2.Error as e:
        print("Error liking tweet:", e)
        return jsonify({'error': 'Error liking tweet'}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/dislikeTweet/<int:tweet_id>/<string:username>', methods=['POST'])
def dislikeTweet(tweet_id, username):

    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Update the dislike count in the database
        cursor.execute("UPDATE Tweet SET likes = likes - 1 WHERE tweet_id = %s AND original_username = %s",
                       (tweet_id, username))
        connection.commit()
        print("dislikeTweet: dislike count updated")

        # Retrieve the updated like count
        cursor.execute("SELECT likes FROM Tweet WHERE tweet_id = %s AND original_username = %s",
                       (tweet_id, username))
        updated_likes = cursor.fetchone()[0]

        return jsonify({'likes': updated_likes})

    except psycopg2.Error as e:
        print("Error disliking tweet:", e)
        return jsonify({'error': 'Error disliking tweet'}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/reshareTweet/<int:tweet_id>/<string:username>', methods=['POST'])
def reshareTweet(tweet_id, username):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Check if the user has already reshared the tweet
        cursor.execute("SELECT * FROM Reshare WHERE resharing_username = %s AND tweeting_username = %s AND tweet_id = %s",
                       (session['username'], username, tweet_id))
        existing_reshare = cursor.fetchone()

        if existing_reshare:
            cursor.execute("DELETE FROM Reshare WHERE resharing_username = %s AND tweeting_username = %s AND tweet_id = %s",
                           (session['username'], username, tweet_id))
            connection.commit()

            # Update the reshare count in the database
            cursor.execute("UPDATE Tweet SET reshares = reshares - 1 WHERE tweet_id = %s AND original_username = %s",
                            (tweet_id, username))
            connection.commit()

            # Retrieve the updated reshare count
            cursor.execute("SELECT reshares FROM Tweet WHERE tweet_id = %s AND original_username = %s",
                       (tweet_id, username))
            updated_reshares = cursor.fetchone()[0]
            
            return jsonify({'reshares': updated_reshares})

        # Insert the reshare record into the database
        cursor.execute("INSERT INTO Reshare VALUES (%s, %s, %s)",
                       (session['username'], username, tweet_id))
        connection.commit()

        # Update the reshare count in the database
        cursor.execute("UPDATE Tweet SET reshares = reshares + 1 WHERE tweet_id = %s AND original_username = %s",
                       (tweet_id, username))
        connection.commit()

        # Retrieve the updated reshare count
        cursor.execute("SELECT reshares FROM Tweet WHERE tweet_id = %s AND original_username = %s",
                       (tweet_id, username))
        updated_reshares = cursor.fetchone()[0]

        return jsonify({'reshares': updated_reshares})

    except psycopg2.Error as e:
        print("Error resharing tweet:", e)
        return jsonify({'error': 'Error resharing tweet'}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/followUser/<string:username>', methods=['POST', 'GET'])
def followUser(username):
    if 'username' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO Follow VALUES (%s, %s)", (session['username'], username))
            connection.commit()

        except psycopg2.Error as e:
            print("Error following user:", e)
            # flash('Error following user', 'error')

        finally:
            cursor.close()
            connection.close()


@app.route('/unfollowUser/<string:following_username>', methods=['POST', 'GET'])
def unfollowUser(following_username):
    if request.method == 'POST':
       if 'username' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM Follow WHERE follower_username = %s AND following_username = %s", (session['username'], following_username))
            connection.commit()

        except psycopg2.Error as e:
            print("Error following user:", e)
            # flash('Error following user', 'error')

        finally:
            cursor.close()
            connection.close()


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
        # flash('User does not exist', 'error')

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('start_page'))



@app.route('/deleteTweet/<int:tweet_id>', methods=['POST'])
def deleteTweet(tweet_id):
    if request.method == 'POST':
        username = session.get('username')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Check if the tweet belongs to the logged-in user
            # Delete the tweet
            cursor.execute("DELETE FROM Tweet WHERE original_username = %s AND tweet_id = %s", (session['username'], tweet_id))
            connection.commit()

            # flash('Tweet deleted successfully', 'success')
            # else:
            # flash('Unauthorized to delete this tweet', 'error')

        except psycopg2.Error as e:
            print("Error deleting tweet:", e)
            flash('Error deleting tweet', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('homepage'))


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


# Add a new route and functions for editing settings
@app.route('/updateSettings', methods=['POST'])
def updateSettings():
    if request.method == 'POST':
        # Retrieve form data from the request
        new_password = request.form['new_password']
        new_email = request.form['new_email']
        new_display_name = request.form['new_display_name']

        # Get the current username from the session
        username = session.get('username')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Update the user's settings in the database
            cursor.execute("UPDATE Usr SET password = %s, email = %s, display_name = %s WHERE username = %s",
                           (new_password, new_email, new_display_name, username))
            connection.commit()

            # flash('Settings updated successfully', 'success')

        except psycopg2.Error as e:
            print("Error updating settings:", e)
            # flash('Error updating settings', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('settings_page'))

@app.route('/deleteComment', methods=['POST'])
def deleteComment():
    commenting_username = session.get('username')
    timestmp = request.form.get('timestmp')
    timestmp_datetime = datetime.strptime(timestmp, '%Y-%m-%d %H:%M:%S')

    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Check if the comment belongs to the logged-in user
        cursor.execute("SELECT commenting_username FROM Cmmnt WHERE commenting_username = %s AND timestmp = %s",
                       (commenting_username, timestmp_datetime))
        comment_owner = cursor.fetchone()

        if comment_owner and comment_owner[0] == commenting_username:
            # Delete the comment
            cursor.execute("DELETE FROM Cmmnt WHERE commenting_username = %s AND timestmp = %s",
                           (commenting_username, timestmp_datetime))
            connection.commit()

            # flash('Comment deleted successfully', 'success')
        else:
            flash('Unauthorized to delete this comment', 'error')

    except psycopg2.Error as e:
        print("Error deleting comment:", e)
        flash('Error deleting comment', 'error')

    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run()
