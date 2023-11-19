class Tweet:
    def __init__(self, tweet_id, original_username, cntnt, likes, reshares, timestmp):
        self.tweet_id = tweet_id 
        self.original_username = original_username
        self.cntnt = cntnt
        self.likes = likes 
        self.reshares = reshares
        self.timestmp = timestmp