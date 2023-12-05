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
VALUES ('alice_123', 'pass123', '2023-11-11', 'alice123@example.com', 'Alice', 'uploads/Saharsh-Cat.png', '2005-03-15');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('bob_rider', 'securePass', '2023-11-14', 'bob.rider@example.com', 'Bob', 'images/profile_picture.jpg', '2008-07-22');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('charlie_blue', 'random123', '2023-11-18', 'charlie.blue@example.com', 'Charlie', 'images/profile_picture.jpg', '2002-11-09');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('diana_rose', 'pass_diana', '2023-11-20', 'diana.rose@example.com', 'Diana', 'images/profile_picture.jpg', '2007-04-18');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('edward23', 'ePass', '2023-11-23', 'edward_23@example.com', 'Edward', 'images/profile_picture.jpg', '2004-09-27');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('fiona_g', 'fiona_pass', '2023-11-25', 'fiona.g@example.com', 'Fiona', 'images/profile_picture.jpg', '2006-01-12');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('george45', 'george_pass', '2023-11-28', 'george45@example.com', 'George', 'images/profile_picture.jpg', '2009-08-05');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('hannah.green', 'hannah_pass', '2023-12-01', 'hannah.green@example.com', 'Hannah', 'uploads/Mitsu-Post.jpeg', '2003-06-30');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('isaac98', 'isaac_pass', '2023-12-05', 'isaac98@example.com', 'Isaac', 'uploads/Hotpot.png', '2001-02-14');

INSERT INTO Usr (username, password, account_creation_date, email, display_name, profile_picture, birthday)
VALUES ('julia_music', 'julia_pass', '2023-12-08', 'julia.music@example.com', 'Julia', 'uploads/Mitsu-Cat.jpeg', '2000-10-08');

-- Populating Tweet Table
-- Alice's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('alice_123', 1, 'Just joined TwitFace! Excited to tweet! 🐦', 8, 0, '2023-11-15 14:24:01');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('alice_123', 2, 'Just enjoying a cup of coffee. ☕', 15, 0, '2023-11-20 08:45:30');

-- Bob's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('bob_rider', 1, 'First tweet! Hello TwitFace world! 👋', 12, 0, '2023-11-16 09:30:00');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('bob_rider', 2, 'Monday blues hitting hard. 😓', 8, 0, '2023-11-18 16:30:45');

-- Charlie's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('charlie_blue', 1, 'Tweeting for the first time! #Newbie', 5, 0, '2023-11-17 12:12:12');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('charlie_blue', 2, 'Coding session in progress! 💻', 5, 0, '2023-11-19 12:12:12');

-- Diana's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('diana_rose', 1, 'First tweet! Excited to share thoughts. 😊', 10, 0, '2023-11-16 18:05:03');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('diana_rose', 2, 'Exploring new book genres. Any recommendations? 📚', 12, 0, '2023-11-17 21:05:03');

-- Edward's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('edward23', 1, 'Hello TwitFace! Ready to share my thoughts. 😄', 6, 0, '2023-11-15 10:28:55');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('edward23', 2, 'Weekend adventures await! 🌲🚗', 10, 0, '2023-11-16 09:28:55');

-- Fiona's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('fiona_g', 1, 'First tweet! Excited to share my journey. 🌟', 7, 0, '2023-11-15 15:40:20');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('fiona_g', 2, 'Trying out a new recipe tonight. Wish me luck! 🍲', 18, 0, '2023-11-15 18:40:20');

-- George's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('george45', 1, 'Hey TwitFace! Excited to start tweeting. 😎', 14, 0, '2023-11-18 07:55:10');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('george45', 2, 'Gym session complete! 💪 #FitnessFriday', 25, 0, '2023-11-21 07:55:10');

-- Hannah's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('hannah.green', 1, 'First tweet! Let the tweeting begin! 😊', 9, 0, '2023-11-16 12:15:48');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('hannah.green', 2, 'Movie night with friends. 🍿🎬', 30, 0, '2023-11-22 22:15:48');

-- Isaac's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('isaac98', 1, 'Hello TwitFace! Ready to share my thoughts. 🌟', 11, 0, '2023-11-19 14:37:29');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('isaac98', 2, 'Learning a new language. Any language-learning tips? 🌐', 22, 0, '2023-11-20 14:37:29');

-- Julia's tweets
INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('julia_music', 1, 'First tweet! Excited to share my love for music. 🎶', 15, 0, '2023-11-17 10:10:05');

INSERT INTO Tweet (original_username, tweet_id, cntnt, likes, reshares, timestmp)
VALUES ('julia_music', 2, 'Music is my therapy. What is your favorite genre? 🎶', 16, 0, '2023-11-19 10:10:05');



-- Populating Reshare Table
-- INSERT INTO Reshare (resharing_username, tweeting_username, tweet_id)
-- VALUES ('username2', 'username1', 1);

-- Populating Cmmnt Table
-- Alice's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('diana_rose', 'alice_123', 1, '2023-11-15 19:30:00', 'Your first tweet is relatable, Alice! Cheers to coffee lovers.');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('george45', 'alice_123', 2, '2023-11-20 13:45:30', 'Your second tweet is fantastic, Alice! Keep it up.');

-- Bob's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('hannah.green', 'bob_rider', 1, '2023-11-16 11:55:30', 'Monday blues are tough, Bob. Hope your day gets better.');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('julia_music', 'bob_rider', 2, '2023-11-21 10:10:15', 'Your second tweet is music to my ears, Bob! Keep rocking.');

-- Charlie's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('fiona_g', 'charlie_blue', 1, '2023-11-17 15:15:18', 'Coding is an art, Charlie! Your first tweet resonates with me.');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('isaac98', 'charlie_blue', 2, '2023-11-22 11:30:45', 'Your second tweet showcases dedication, Charlie! Keep coding.');

-- Diana's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('edward23', 'diana_rose', 1, '2023-11-18 13:20:45', 'Your first tweet sparked my interest, Diana! Any book recommendations?');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('julia_music', 'diana_rose', 2, '2023-11-23 11:45:10', 'Your second tweet struck a chord, Diana! What inspires your reading choices?');

-- Edward's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('george45', 'edward23', 1, '2023-11-19 09:45:30', 'Weekend adventures are the best, Edward! Enjoy every moment.');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('fiona_g', 'edward23', 2, '2023-11-24 08:20:15', 'Your second tweet radiates positivity, Edward! Keep spreading joy.');

-- Fiona's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('hannah.green', 'fiona_g', 1, '2023-11-15 16:55:10', 'Your first tweet is filled with excitement, Fiona! Cannot wait to see more.');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('julia_music', 'fiona_g', 2, '2023-11-23 14:35:48', 'Your second tweet resonates with my love for trying new recipes, Fiona!');

-- George's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('isaac98', 'george45', 1, '2023-11-20 10:55:45', 'Your first tweet exudes coolness, George! Keep the vibe.');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('hannah.green', 'george45', 2, '2023-11-25 09:30:20', 'Your second tweet about fitness is inspiring, George! Keep it up.');

-- Hannah's tweets
INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('julia_music', 'hannah.green', 1, '2023-11-16 13:05:48', 'Your first tweet brings a smile, Hannah! Movie nights are the best.');

INSERT INTO Cmmnt (commenting_username, tweeting_username, tweet_id, timestmp, comment_content)
VALUES ('isaac98', 'hannah.green', 2, '2023-11-26 07:50:10', 'Your second tweet sounds like a fantastic language-learning journey.');

-- Populating Media Table
INSERT INTO Media (username, tweet_id, media_url)
VALUES ('bob_rider', 1, '/images/Saharsh-Post.jpeg');

INSERT INTO Media (username, tweet_id, media_url)
VALUES ('alice_123', 2, '/images/coffee.jpeg');

INSERT INTO Media (username, tweet_id, media_url)
VALUES ('isaac98', 1, 'uploads/pic1.jpeg');

-- Populating Follow Table
-- Random Follow Queries
INSERT INTO Follow (follower_username, following_username)
VALUES ('alice_123', 'bob_rider');

INSERT INTO Follow (follower_username, following_username)
VALUES ('bob_rider', 'charlie_blue');

INSERT INTO Follow (follower_username, following_username)
VALUES ('charlie_blue', 'diana_rose');

INSERT INTO Follow (follower_username, following_username)
VALUES ('diana_rose', 'edward23');

INSERT INTO Follow (follower_username, following_username)
VALUES ('edward23', 'fiona_g');

INSERT INTO Follow (follower_username, following_username)
VALUES ('fiona_g', 'george45');

INSERT INTO Follow (follower_username, following_username)
VALUES ('george45', 'hannah.green');

INSERT INTO Follow (follower_username, following_username)
VALUES ('hannah.green', 'isaac98');

INSERT INTO Follow (follower_username, following_username)
VALUES ('isaac98', 'julia_music');

INSERT INTO Follow (follower_username, following_username)
VALUES ('julia_music', 'alice_123');

