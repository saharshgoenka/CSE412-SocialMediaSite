-- ++TABLE CREATION ++

-- TABLE SCHEMA 
-- Name: Usr
-- Attributes (username, password, account_creation_date, email, display_name, profile_picture, birthday)
CREATE TABLE Usr (
    username text PRIMARY KEY,
    password text NOT NULL,
    account_creation_date DATE,
    email text NOT NULL,
    display_name text,
    profile_picture text,
    birthday DATE
);

-- TABLE SCHEMA
-- Name: Tweet
-- Attributes (original_username, tweet_id, cntnt, likes, reshares, timestmp)
CREATE TABLE Tweet (
    original_username text,
    tweet_id INT,
    cntnt TEXT NOT NULL,
    likes INT NOT NULL,
    reshares INT NOT NULL,
    timestmp TIMESTAMP NOT NULL,
    PRIMARY KEY (original_username, tweet_id),
    FOREIGN KEY (original_username) REFERENCES Usr(username)
    ON DELETE CASCADE
);

-- TABLE SCHEMA
-- Name: Reshare
-- Attributes (resharing_username, tweeting_username, tweet_id)
CREATE TABLE Reshare (
    resharing_username text,
    tweeting_username text,
    tweet_id INT,
    PRIMARY KEY (resharing_username, tweeting_username, tweet_id),
    FOREIGN KEY (resharing_username) REFERENCES Usr(username)
    ON DELETE CASCADE,
    FOREIGN KEY (tweeting_username) REFERENCES Usr(username)
    ON DELETE CASCADE,
    FOREIGN KEY (tweeting_username, tweet_id) REFERENCES Tweet(original_username, tweet_id)
    ON DELETE CASCADE
);

-- TABLE SCHEMA
-- Name: Media
-- Attributes (username, tweet_id, media_url)
CREATE TABLE Media (
    username text,
    tweet_id INT,
    media_url text NOT NULL,
    PRIMARY KEY (username, tweet_id, media_url),
    FOREIGN KEY (username) REFERENCES Usr(username)
    ON DELETE CASCADE,
    FOREIGN KEY (username, tweet_id) REFERENCES Tweet(original_username, tweet_id)
    ON DELETE CASCADE
);

-- TABLE SCHEMA
-- Name: Cmmnt
-- Attributes (commenting_username, tweeting_username, tweet_id, timestmp comment_content)
CREATE TABLE Cmmnt (
    commenting_username text,
    tweeting_username text,
    tweet_id INT,
    timestmp TIMESTAMP,
    comment_content text NOT NULL,
    PRIMARY KEY (commenting_username, tweeting_username, tweet_id, timestmp)
    FOREIGN KEY (commenting_username) REFERENCES Usr(username)
    ON DELETE CASCADE,
    FOREIGN KEY (tweeting_username) REFERENCES Usr(username)
    ON DELETE CASCADE,
    FOREIGN KEY (tweeting_username, tweet_id) REFERENCES Tweet(original_username, tweet_id)
    ON DELETE CASCADE
);

-- TABLE SCHEMA
-- Name: Follow
-- Attributes (follower_username, following_username)
CREATE TABLE Follow (
    follower_username text NOT NULL,
    following_username text NOT NULL,
    PRIMARY KEY (follower_username, following_username),
    FOREIGN KEY (follower_username) REFERENCES Usr(username)
    ON DELETE CASCADE,
    FOREIGN KEY (following_username) REFERENCES Usr(username)
    ON DELETE CASCADE
);

-- --END OF TABLE CREATION --

-- ++TABLE POPULATION START ++
-- Populating Usr Table
COPY Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday) FROM stdin;
'username1'     'password1'     '2023-11-10'        'user1@example.com'     'User 1'        'pfp_fpath'     '1999-01-01'
'username2'     'password2'     '2023-11-11'        'user2@example.com'     'User 2'        'pfp_fpath'     '1999-01-02'
'username3'     'password3'     '2023-11-11'        'user3@example.com'     'User 3'        'pfp_fpath'     '1999-01-03'
'username4'     'password4'     '2023-11-11'        'user4@example.com'     'User 4'        'pfp_fpath'     '1999-01-04'
'username5'     'password5'     '2023-11-11'        'user5@example.com'     'User 5'        'pfp_fpath'     '1999-01-05'
'username6'     'password6'     '2023-11-11'        'user6@example.com'     'User 6'        'pfp_fpath'     '1999-01-06'
\.

-- Populating Tweet Table
COPY Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp) FROM stdin;
'username1'     1       "User 1's first tweet!"         0       0       '2023-11-15 14:24:01'
'username1'     2       "User 1's second tweet!"        0       0       '2023-11-16 13:20:05'
'username1'     3       "User 1's third tweet!"         0       0       '2023-11-16 17:21:10'
'username2'     1       "User 2's first tweet!"         0       0       '2023-13-01 11:10:05'
'username4'     1       "User 4's first tweet!"         0       0       '2023-12-03 01:10:14'
'username5'     1       "User 5's first tweet!"         0       0       '2023-16-01 10:10:10'
\.

-- Populating Reshare Table
COPY Reshare (resharing_username, tweeting_username, tweet_id) FROM stdin;