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
    PRIMARY KEY (commenting_username, tweeting_username, tweet_id, timestmp),
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
INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('username1', 'password1', '2023-11-10', 'user1@example.com', 'User 1', 'pfp_fpath', '1999-01-01');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('username2', 'password2', '2023-11-11', 'user2@example.com', 'User 2', 'pfp_fpath', '1999-01-02');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('username3', 'password3', '2023-11-11', 'user3@example.com', 'User 3', 'pfp_fpath', '1999-01-03');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('username4', 'password4', '2023-11-11', 'user4@example.com', 'User 4', 'pfp_fpath', '1999-01-04');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('username5', 'password5', '2023-11-11', 'user5@example.com', 'User 5', 'pfp_fpath', '1999-01-05');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('username6', 'password6', '2023-11-11', 'user6@example.com', 'User 6', 'pfp_fpath', '1999-01-06');


-- Populating Tweet Table
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('username1', 1, 'User 1''s first tweet!', 0, 0, '2023-11-15 14:24:01');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('username1', 2, 'User 1''s second tweet!', 0, 0, '2023-11-16 13:20:05');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('username1', 3, 'User 1''s third tweet!', 0, 0, '2023-11-16 17:21:10');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('username2', 1, 'User 2''s first tweet!', 0, 0, '2023-12-01 11:10:05');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('username4', 1, 'User 4''s first tweet!', 0, 0, '2023-12-03 01:10:14');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('username5', 1, 'User 5''s first tweet!', 0, 0, '2023-10-01 10:10:10');


-- Populating Reshare Table
INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
VALUES ('username2', 'username1', 1);

INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
VALUES ('username3', 'username1', 1);

INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
VALUES ('username4', 'username2', 1);

INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
VALUES ('username6', 'username1', 3);

INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
VALUES ('username1', 'username4', 1);

INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
VALUES ('username3', 'username5', 1);

INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
VALUES ('username5', 'username1', 2);

-- Populating Cmmnt Table
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('username1', 'username2', 1, '2023-11-18 15:31:01', 'User 1 commented on User 2''s first tweet');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('username2', 'username1', 3, '2023-11-14 10:01:52', 'User 2 commented on User 1''s third tweet');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('username6', 'username5', 1, '2023-11-17 05:10:18', 'User 6 commented on User 5''s first tweet');

-- Populating Media Table
INSERT INTO Media (username, tweet_id, media_url)
VALUES ('username1', 1, "fpath to a file")

-- Populating Follow Table
INSERT INTO Follow (follower_username, following_username)
VALUES ('username1', 'username2');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username1', 'username3');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username1', 'username4');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username2', 'username1');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username2', 'username4');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username3', 'username1');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username3', 'username2');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username4', 'username1');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username4', 'username2');

INSERT INTO Follow (follower_username, following_username)
VALUES ('username5', 'username1');
