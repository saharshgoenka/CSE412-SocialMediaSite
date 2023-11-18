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
def start_page():
    return render_template('loadpage.html')

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

@app.route('/create_user', methods=['POST'])
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

if __name__ == '__main__':
    app.run()
