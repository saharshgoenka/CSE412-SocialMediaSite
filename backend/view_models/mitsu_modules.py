from models import Comment
from models.Tweet import Tweet
from models.Comment import Comment
import psycopg2

def create_db_connection():
	connection = psycopg2.connect(
        user='mitsuakifukuzaki',
		host="/tmp",
		port="5432",
		database="mitsuakifukuzaki"
	)
	return connection

def createUser():
    cmmnt = Comment( 'usename1', 'username2', 1, '1', 'test')

    print(cmmnt.commenting_username)


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

        return comment_list
            
    except psycopg2.Error as e:
        print("Error:", e)

loadUsersComments('username1')