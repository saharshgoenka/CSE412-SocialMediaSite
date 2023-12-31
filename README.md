# Twitface User Manual
TwitFace is an academic project created for CSE 412 - Database Management. The goal of this application is to provide users with a platform on which they may interact with other users across the globe and create their own social networks. Users may post, comment, follow, reshare, and like other users' content.

# Setup
### Cloning the Repository
1. Create a folder in an easily accessible location. Name it whatever you like.
2. Open your terminal
3. Change directories until inside the folder you just created. Recall cd {directory}
4. Once inside of the folder, run the following command:

`git clone https://github.com/saharshgoenka/CSE412-SocialMediaSite.git`

5. Confirm that the cloning was successfully run by executing the following command:

`ls`
- You should see the name 'CSE412-SocialMediaSite'

### Downloading Dependencies
1. Enter 'CSE412-SocialMediaSite' by running:

`cd CSE412-SocialMediaSite`
2. Once inside, run the following command:

`pip3 install --user -r dependencies.txt`

### Setting up the Database
1. Change directories back to the original folder you created.
2. Create a new folder. Name it something fitting for a database. e.g. "DatabaseFolder"
3. Copy the file path to this newly created folder. Ensure the folder name is within the copied path.
4. Enter the following commands into your terminal:

`export PATH="/Library/PostgreSQL/15/bin:${PATH}"`

`cd `

`export PGPORT=5432`

`export PGHOST=/tmp`

`initdb {PASTE THE COPIED PATH, remove curly braces}`

`pg_ctl -D {PASTE FOLDER PATH} -o '-k /tmp' start`

`createdb $USER`

`cd CSE412-SocialMediaSite`

5. Open up the REPO on Visual Studio Code
6. Navigate to the makefile stored in init_db
7. Change the following line:

`SRC_DIRECTORY = COPY PASTE PATH TO init_db`

8. Save the file
9. In your terminal, change directories to the init_db folder
10. Run make setup_postgres
11. Confirm that the database was successfully loaded by running the following commands:

`psql -d $USER`
`SELECT * From Usr;`

### Additional Setup
1. Navigate to app.py found in the flask folder of the REPO
2. Change the database accessing fields found on lines 25-28 to:

- user={username found in the terminal history}
- host='/tmp'
- port=5432
- database={same as user}

# Walkthrough and Navigation

Once the setup is complete, the user can run the application by going into the flask folder and typing ```python3 app.py```. The user can then navigate to ```127.0.0.1:5000``` on any browser where they can start interacting with the application.


## Login Page
![Login Page Screenshot](screenshots/LogIn-Page.png)

Entering a valid username and password combo will allow access to the homepage.


## Sign Up Page
![Signup Page Screenshot](screenshots/SignUp-Page.png)

User can insert username, password, email, display name, profile picture(that ends with png, jpg, jpeg) and birthday using the interface. Clicking sign up will create a user with the entered fields.

## Home Page
![Home Page Screenshot](screenshots/Home-Page.png)

The homepage features a series of introductory messages, followed by a "Create Tweet" box. Upon entering tweet content and clicking "Tweet," a tweet is generated. The tweet content may consist of text alone or a combination of text and an image, which can be inserted using the "Choose Image" option. Below the tweet creation box, the database displays all tweets. Each tweet is structured with the username as a blue hyperlink leading to the profile page, and "View Comments" as a blue hyperlink leading to the comments page. Additionally, each tweet includes a count, allowing users to increase or decrease it by pressing the like or dislike buttons. The reshare button enables users to reshare or unshare a tweet with a single click. The content of each tweet is displayed prominently in the middle, and if an image is attached, it is included in the content. At the very bottom are two hyperlinks: "Settings" and "Logout". Clicking logout will lead to the user getting logged out. Thus, the user will be kicked from the home page back to login page. Clicking the settings hyperlink will lead to a settings page.

## Profile Page
![Profile Page Screenshot](screenshots/Profile-Page.png)
Clicking on the username hyperlink on the homepage redirects users to the profile page. The profile page is structured with user details followed by the tweets of the specific user. Additionally, a follow/unfollow button is prominently displayed when visiting other users' pages. If the user was previously following this profile, it will indicate "following"; otherwise, the button will display "follow." By clicking the follow button, the user becomes a follower of the displayed profile, and the button transforms into "following." To unfollow, users simply click the button again, reverting it back to "Follow." The "Shared Tweets" section shows all tweets that the user has posted and reshared.

## Comments Page
![Comments Page Screenshot](screenshots/Comments-Page.png)
Clicking "View Comments" on the homepage directs users to the comments page. This page displays the tweet from the homepage that led to it, along with all comments on that tweet. Each comment includes a username, content, timestamp of when it was posted and a delete comment button. Pressing delete comment will allow the user to delete a comment if the user owns it. If the user does not own the comment that button will not be shown. Below the comments, a text box allows users to enter comment content and post it by clicking "Post Comment". Lastly, there is a delete tweet button at the very button which appears if the user owns the tweet. Pressing delete tweet will delete the tweet and all comments associated with it.

## Settings Page
![Settings Page Screenshot](screenshots/Settings-Page.png)
The settings page allows the user to edit password, email and display_name. Pressing "Save Changes" will save these changes. There is also a "Delete Account" button. Pressing that will lead to deletion of the entire usr table and all data related to the usr table will be purged.
