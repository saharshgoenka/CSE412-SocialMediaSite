# CSE412 Final Project-Twitface

# Walkthrough and Navigation

Once the setup is complete, the user can run the application by going into the flask folder and typing ```python3 app.py```. The user can then navigate to ```127.0.0.1:5000``` on any browser where they can start interacting with the application.

## Sign Up Page

User can insert username, password, email, display name, profile picture(that ends with png, jpg, jpeg) and birthday using the interface. Clicking sign up will create a user with the entered fields. 

## Login Page

Entering a valid username and password combo will allow access to the homepage.

## Home Page

```markdown
**Homepage Features:**
- Create tweets with text or text and images.
- Hyperlinked usernames to profile pages.
- View Comments hyperlinks to the comments page.
- Like and dislike functionality with reshare option.
- Display of attached images with tweets.

Homepage has a series of introductory messages followed by a create tweet box. Entering tweet content and clicking "Tweet" will create a tweet. The tweet content can either just be text or can be a combination of text and an image, which can be inserted using "Choose Image". Underneath the create tweet box are all the tweets in the database. Each tweet is structured in a way such that the username (blue hyperlink) is a link to the profile page. Similarly, View Comments (blue hyperlink) is a link to the comments page. Each tweet also contains a count. Pressing like increases the count, and pressing dislike decreases the count. Similarly, each tweet has a reshare button. Clicking once results in a reshare, and clicking again results in an unshare. Finally, each tweet displays the content in the middle. If an image was attached to a tweet, the content will include the attached image.

## Profile Page

Profile Page has user details followed by that particular user's tweets. There is also a follow/unfollow button. If the user was previously following the user, it will show up as following; else, the button will show up as follow. Pressing follow will make it so the user follows the user whose profile is being displayed. The button will change to following. To unfollow, the user presses the button again, and it will change back to Follow.

