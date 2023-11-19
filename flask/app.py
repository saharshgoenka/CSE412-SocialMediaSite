from flask import Flask, Response, url_for, redirect, render_template, request, session, flash, jsonify
import psycopg2

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

if __name__ == '__main__':
    app.run()
