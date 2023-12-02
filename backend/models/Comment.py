class Comment:
    commenting_username:str
    tweeting_username:str 
    tweet_id:int
    timestmp:str
    comment_content:str

    def __init__(self, commenting_username:str, tweeting_username:str, tweet_id:int, timestmp:str, comment_content:str):
        self.commenting_username = commenting_username
        self.tweeting_username = tweeting_username
        self.tweet_id = tweet_id
        self.timestmp = timestmp
        self.comment_content = comment_content
        