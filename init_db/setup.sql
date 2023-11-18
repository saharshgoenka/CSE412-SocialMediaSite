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
-- Attributes (tweet_id, original_username, cntnt, likes, reshares, timestmp)
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
