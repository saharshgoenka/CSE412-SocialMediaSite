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

        print(comments)
    except psycopg2.Error as e:
        print("Error:", e)

loadUsersComments('username1')