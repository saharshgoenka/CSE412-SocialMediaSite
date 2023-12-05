# CSE412 Final Project-Twitface

# Walkthrough and Navigation

Once the setup is complete, the user can run the application by going into the flask folder and typing ```python3 app.py```. The user can then navigate to ```127.0.0.1:5000``` on any browser where they can start interacting with the application.

## Sign Up Page

User can insert username, password, email, display name, profile picture(that ends with png, jpg, jpeg) and birthday using the interface. Clicking sign up will create a user with the entered fields. 

## Login Page

Entering a valid username and password combo will allow access to the homepage.

## Home Page

The homepage features a series of introductory messages, followed by a "Create Tweet" box. Upon entering tweet content and clicking "Tweet," a tweet is generated. The tweet content may consist of text alone or a combination of text and an image, which can be inserted using the "Choose Image" option. Below the tweet creation box, the database displays all tweets. Each tweet is structured with the username as a blue hyperlink leading to the profile page, and "View Comments" as a blue hyperlink leading to the comments page. Additionally, each tweet includes a count, allowing users to increase or decrease it by pressing the like or dislike buttons. The reshare button enables users to reshare or unshare a tweet with a single click. The content of each tweet is displayed prominently in the middle, and if an image is attached, it is included in the content.

## Profile Page

Clicking on the username hyperlink on the homepage redirects users to the profile page. The profile page is structured with user details followed by the tweets of the specific user. Additionally, a follow/unfollow button is prominently displayed. If the user was previously following this profile, it will indicate "following"; otherwise, the button will display "follow." By clicking the follow button, the user becomes a follower of the displayed profile, and the button transforms into "following." To unfollow, users simply click the button again, reverting it back to "Follow."

## Comments Page

Clicking "View Comments" on the homepage directs users to the comments page. This page displays the tweet from the homepage that led to it, along with all comments on that tweet. Each comment includes a username, content, and timestamp of posting. Below the comments, a text box allows users to enter comment content and post it by clicking "Post Comment."