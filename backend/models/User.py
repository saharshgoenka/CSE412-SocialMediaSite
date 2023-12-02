"""
User Class: Used to store user information
"""

class User:
    def __init__(self, username: str, password: str, account_creation_date: str, email: str, display_name: str, profile_picture: str, birthday: str):
        self.username = username
        self.password = password
        self.account_creation_date = account_creation_date
        self.email = email
        self.display_name = display_name
        self.profile_picture = profile_picture
        self.birthday = birthday