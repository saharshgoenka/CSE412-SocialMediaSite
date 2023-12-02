import sys
sys.path.append('/Users/enigma/Desktop/ASU2023/Fall2023/CSE412/FinalProject/CSE412-SocialMediaSite/backend')

from models.User import User
from models.Tweet import Tweet
from models.Comment import Comment

user2 = User(
        "jane_doe",
        "strong_password",
        "2023-02-15",
        "jane.doe@example.com",
        "Jane Doe",
        "jane_profile.jpg",
        "1985-05-20"
    )

# Accessing attributes
print(user2.username)
print(user2.email)

# Print the user object
print(user2)