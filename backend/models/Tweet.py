"""
Tweet Class: Used to store tweet information
"""

class User:
    def __init__(self, original_username: str, tweet_id: int, cntnt: str, likes: int, reshares: int, timestmp:str):
        self.original_username = original_username
        self.tweet_id = tweet_id
        self.cntnt = cntnt
        self.likes = likes
        self.reshares = reshares
        self.timestmp = timestmp