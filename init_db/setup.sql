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

-- TABLE SCHEMA
-- Name: Reshare
-- Attributes (resharing_username, tweeting_username, tweet_id)

-- TABLE SCHEMA
-- Name: Media
-- Attributes (username, tweet_id, media_url)

-- TABLE SCHEMA
-- Name: Cmmnt
-- Attributes (commenting_username, tweeting_username, tweet_id, timestmp comment_content)

-- TABLE SCHEMA
-- Name: Follow
-- Attributes (follower_username, following_username)
