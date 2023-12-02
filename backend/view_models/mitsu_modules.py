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

def createComment(commenting_username:str, tweeting_username:str, tweet_ID:int, comment_content:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        timestmp_intermediate = datetime.now()
        
        timestmp = timestmp_intermediate.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE Cmmnt SET comment_content = %s WHERE commenting_username = %s AND tweeting_username = %s AND tweet_id = %s AND timestmp = %s", (commenting_username, tweeting_username, tweet_ID, timestmp, comment_content))
    
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        connection.commit();
        cursor.close()
        connection.close()

def editComment(commenting_username:str, tweeting_username:str, tweet_ID:int, timestamp:str, new_content:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE Cmmnt SET comment_content = %s WHERE commenting_username = %s AND tweeting_username = %s AND tweet_id = %s AND timestmp = %s", (new_content, commenting_username, tweeting_username, tweet_ID, timestamp))
    
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        connection.commit();
        cursor.close()
        connection.close()

def deleteComment(commenting_username:str, tweeting_username:str, tweet_ID:int, timestamp:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Cmmnt WHERE commenting_username = %s AND tweeting_username = %s AND tweet_id = %s AND timestmp = %s", (commenting_username, tweeting_username, tweet_ID, timestamp))
    
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        connection.commit();
        cursor.close()
        connection.close()

def loadUsersComments(commenting_username:str):
    connection = create_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Cmmnt WHERE commenting_username = %s", (commenting_username, ))
        comments = cursor.fetchall()

        comment_list = []
        for comment in comments:
            commenting_username_temp = comment[0]
            tweeting_username_temp   = comment[1]
            tweet_id_temp            = comment[2]
            timestmp_temp            = comment[3]
            comment_content_temp     = comment[4]

            new_comment = Comment(commenting_username=commenting_username_temp,
                                  tweeting_username=tweeting_username_temp,
                                  tweet_id=tweet_id_temp,
                                  timestmp=timestmp_temp,
                                  comment_content=comment_content_temp)
            
            comment_list.append(new_comment)

        print(len(comment_list))
            
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        connection.commit()
        cursor.close()
        connection.close()
