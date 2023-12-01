from flask import Flask, Response, url_for, redirect, render_template, request, session, flash, jsonify
import psycopg2
import datetime

app = Flask(__name__)
app.secret_key = "secret_key"

def create_db_connection():
	connection = psycopg2.connect(
        user='mitsuakifukuzaki',
		host="/tmp",
		port="8888",
		database="mitsuakifukuzaki"
	)
	return connection

@app.route('/')
def start_page():
    return render_template('loadpage.html')

@app.route('/test/<string:username>', methods=['GET'])
def test(username):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Usr WHERE username = %s", (username, ))
        users = cursor.fetchall()

        formatted_users = {}

        for user in users:
            formatted_users[user[0]] = user

        return jsonify(users)
    except psycopg2.Error as e:
        print("Error:", e)
        flash('Error', 'error')

@app.route('/login', methods=['POST'])
def check_credentials():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Retrieve the user's information based on the provided username
            cursor.execute("SELECT username, password FROM Usr WHERE username = %s", (username,))
            user = cursor.fetchall()

            errors = {'username': True, 'password': True}

            # Check if the user exists and the password is correct
            if user:
                errors['username'] = False  # Username is valid

                if user[1] == password:  # Note: Index 1 corresponds to the password field in the tuple
                    errors['password'] = False  # Password is valid

            # Handle the result as needed
            if not any(errors.values()):
                session['username'] = username
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')

        except psycopg2.Error as e:
            print("Error checking credentials:", e)
            flash('Error checking credentials', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

@app.route('/create_user/<string:username>/<string:password>/<string:email>/', methods=['POST'])
def create_user():
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

#NOT DONE YET 
@app.route('/loadUsersTweet/<string:username>', methods=['GET', 'POST'])
def loadUsersTweet(username):
    if request.method == 'POST' | request.method == 'GET':
        # username = request.form('username')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * FROM Tweet WHERE original_username = %s', (username, ))

            # Returns a table containing all tweets associated to the specified user
            tweet_intermediate = cursor.fetchall()
            # tweet = {
            #             'tweet_id' : tweet_intermediate[0],
            #             'original_username' : tweet_intermediate[1],
            #             'cntnt' : tweet_intermediate[2],
            #             'likes' : tweet_intermediate[3],
            #             'reshares' : tweet_intermediate[4],
            #             'timestmp' : tweet_intermediate[5]
            #         } 

            flash("Tweet Load was successful.", "success")

            # return jsonify(tweet)
        except psycopg2.Error as e:
            print("Error loading tweet:", e)
            flash("Error loading tweet", 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

#DONE
@app.route('/loadTweet/<string:username>/<int:tweet_id>', methods=['GET'])
def loadTweet(username, tweet_id):
    if request.method == 'GET':
        # username = request.form('username')
        # tweet_id = request.form('tweet_id')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * FROM Tweet WHERE original_username = %s AND tweet_id = %i', (username, tweet_id))

            tweet_intermediate = cursor.fetchall()
            tweet = {
                        'tweet_id' : tweet_intermediate[0],
                        'original_username' : tweet_intermediate[1],
                        'cntnt' : tweet_intermediate[2],
                        'likes' : tweet_intermediate[3],
                        'reshares' : tweet_intermediate[4],
                        'timestmp' : tweet_intermediate[5]
                    } 

            flash("Tweet Load was successful.", "success")

            return jsonify(tweet)
        except psycopg2.Error as e:
            print("Error loading tweet:", e)
            flash("Error loading tweet", 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

#DONE
@app.route('/createComment', methods=['POST'])
def createComment():
    if request.method == 'POST':
        commenting_username = session.get('username')
        tweeting_username = request.form['tweeting_username']
        tweet_id = request.form['tweet_id']
        content = request.form['new_content']
        timestmp = str(datetime.datetime.now())

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Retrieve the user's information based on the provided username
            cursor.execute("INSERT INTO Cmmnt VALUES (%s, %s, %i, %s, %s)", (commenting_username, tweeting_username, tweet_id, content, timestmp))
            connection.commit()

            flash("Comment Creation was successful", "success")

        except psycopg2.Error as e:
            print("Error editing comment:", e)
            flash('Error editing comment', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

#DONE
@app.route('/editComment', methods=['POST'])
def editComment():
    if request.method == 'POST':
        commenting_username = session.get('username')
        tweeting_username = request.form['tweeting_username']
        tweet_id = request.form['tweet_id']
        new_content = request.form['new_content']

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            # Retrieve the user's information based on the provided username
            cursor.execute("UPDATE Cmmnt SET comment_content = %s WHERE commenting_username = %s AND tweeting_username = %s AND tweet_id = %i", (new_content, commenting_username, tweeting_username, tweet_id))
            connection.commit()

            flash("Comment Edit was successful", "success")

        except psycopg2.Error as e:
            print("Error editing comment:", e)
            flash('Error editing comment', 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

#DONE
@app.route('/deleteComment', methods=['POST'])
def deleteComment():
    if request.method == 'POST':
        commenting_username = session.get('username')
        tweeting_username = request.form('tweeting_username')
        tweet_id = request.form('tweet_id')
        timestmp = request.form('timestamp')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM Cmmnt WHERE commenting_username = %s AND tweeting_username = %s AND tweet_id = %s AND timestmp = %s", (commenting_username, tweeting_username, tweet_id, timestmp))
            connection.commit()

            flash("Comment was successfully deleted", "success")

        except psycopg2.Error as e:
            print("Error creating user:", e)
            flash('Error creating user', 'error')

#DONE
@app.route('/loadUserComments', methods=['GET'])
def loadUserComments():
    if request.method == 'GET':
        commenting_username = session.get('username')

        connection = create_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM Cmmnt WHERE commenting_username = %s", (commenting_username))
            comments = cursor.fetchall()

            cmmnt = {
                        'commenting_username' : comments[0],
                        'tweeting_username' : comments[1],
                        'tweet_id' : comments[2],
                        'timestmp' : comments[3],
                        'comment_content' : comments[4]
                    }
            
            flash("Successfully Loaded User's Comments", "success")

            return jsonify(cmmnt)


        except psycopg2.Error as e:
            print("Error loading user's comments:", e)
            flash("Error loading user's comments", 'error')

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('start_page'))

if __name__ == '__main__':
    app.run()
