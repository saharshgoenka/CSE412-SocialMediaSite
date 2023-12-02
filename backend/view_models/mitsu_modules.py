from models import Comment
from models.Tweet import Tweet
from models.Comment import Comment
import psycopg2
from datetime import datetime

def create_db_connection():
	connection = psycopg2.connect(
        user='mitsuakifukuzaki',
		host="/tmp",
		port="5432",
		database="mitsuakifukuzaki"
	)
	return connection

# Loads a specified user's tweets and returns an array of Tweet Objects
def loadUserTweets(original_username:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Query all tweets associated with a user
        cursor.execute("SELECT * FROM Tweet WHERE original_username = %s", (original_username, ))
        tweets = cursor.fetchall()

        # Iterate through the tweets and create Tweet Objects for each
        tweet_list = []

        # Each Tweet in Tweets is in the following format 
        # (original_username, tweet_ID, cntnt, likes, reshares, timestmp)
        for tweet in tweets:
            original_username_temp = tweet[0],
            tweet_ID_temp          = tweet[1],
            cntnt_temp             = tweet[2],
            likes_temp             = tweet[3],
            reshares_temp          = tweet[4],
            timestmp_temp          = tweet[5]

            # Create a new Tweet Object 
            new_tweet = Tweet(
                                original_username= original_username_temp,
                                tweet_id         = tweet_ID_temp,
                                cntnt            = cntnt_temp,
                                likes            = likes_temp,
                                reshares         = reshares_temp,
                                timestmp         = timestmp_temp
                             )
            
            # Insert the newly created Tweet into the tweet_list
            tweet_list.append(new_tweet)

        # Used to confirm the correct number of tweets were inserted into the array
        print(len(tweet_list))

        # Return the array
        return tweet_list
            
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

def loadTweet(original_username:str, tweet_ID:int):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:

        # Load tweet under specified parameter
        cursor.execute("SELECT * FROM Tweet WHERE original_username = %s AND tweet_id = %s", (original_username, tweet_ID))
        tweet_intermediate = cursor.fetchall()
        
        # Convert to Tweet Object
        tweet = Tweet(
            original_username=tweet_intermediate[0][0],
            tweet_id=tweet_intermediate[0][1],
            cntnt=tweet_intermediate[0][2],
            likes=tweet_intermediate[0][3],
            reshares=tweet_intermediate[0][4],
            timestmp=tweet_intermediate[0][5]
        )
        
        # Return Tweet object
        return tweet
    
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

def createComment(commenting_username:str, tweeting_username:str, tweet_ID:int, comment_content:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Create current time stamp
        timestmp_intermediate = datetime.now()
        timestmp = timestmp_intermediate.strftime("%Y-%m-%d %H:%M:%S")

        # Insert the new comment into DB
        cursor.execute("INSERT INTO Cmmnt(commenting_username, tweeting_username, tweet_id, timestmp, comment_content) VALUES (%s, %s, %s, %s, %s)", (commenting_username, tweeting_username, tweet_ID, timestmp, comment_content))
    
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        # Commit changes
        connection.commit()
        cursor.close()
        connection.close()

def editComment(commenting_username:str, tweeting_username:str, tweet_ID:int, timestamp:str, new_content:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Edit Comments
        cursor.execute("UPDATE Cmmnt SET comment_content = %s WHERE commenting_username = %s AND tweeting_username = %s AND tweet_id = %s AND timestmp = %s", (new_content, commenting_username, tweeting_username, tweet_ID, timestamp))
    
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        # Commit Changes
        connection.commit()
        cursor.close()
        connection.close()

def deleteComment(commenting_username:str, tweeting_username:str, tweet_ID:int, timestamp:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Delete Tweet
        cursor.execute("DELETE FROM Cmmnt WHERE commenting_username = %s AND tweeting_username = %s AND tweet_id = %s AND timestmp = %s", (commenting_username, tweeting_username, tweet_ID, timestamp))
    
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        # Commit Changes
        connection.commit()
        cursor.close()
        connection.close()

def loadUserComments(commenting_username:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        # Load all tweets
        cursor.execute("SELECT * FROM Cmmnt WHERE commenting_username = %s", (commenting_username, ))
        comments = cursor.fetchall()

        # Iterate through the comments and create Comment Objects
        comment_list = []
        for comment in comments:
            commenting_username_temp = comment[0]
            tweeting_username_temp   = comment[1]
            tweet_id_temp            = comment[2]
            timestmp_temp            = comment[3]
            comment_content_temp     = comment[4]

            # Convert the current comment into a Comment Object
            new_comment = Comment(
                                    commenting_username= commenting_username_temp,
                                    tweeting_username  = tweeting_username_temp,
                                    tweet_id           = tweet_id_temp,
                                    timestmp           = timestmp_temp,
                                    comment_content    = comment_content_temp
                                )
            
            # Add the new Comment Object to the array
            comment_list.append(new_comment)

        # Used to confirm the correct number of comments loaded
        print(len(comment_list))

        # return the list of comments
        return comment_list
            
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

loadUserTweets('username1')