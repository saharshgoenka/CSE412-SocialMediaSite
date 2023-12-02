import sys
sys.path.append('/Users/mitsuakifukuzaki/Desktop/Hub/Programming/School/412/CSE412-SocialMediaSite/backend')
from backend.models import Comment
# from models.Tweet import Tweet
# from models.Comment import Comment

def createUser():
    cmmnt = Comment( 'usename1', 'username2', 1, '1', 'test')

    print(cmmnt.commenting_username)

createUser()