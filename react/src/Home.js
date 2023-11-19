// Home.js

import React from 'react';
import Tweet from './Tweet';

const Home = () => {
    const tweets = [
        { id: 1, username: 'user1', content: 'This is my first tweet!' },
        { id: 2, username: 'user2', content: 'Excited to use my social media site!' },
        { id: 3, username: 'user3', content: 'Just added another tweet to the feed!' },
        // Add more tweets as needed
    ];

    return (
        <div className="container mx-auto mt-4">
            {tweets.map((tweet) => (
                <Tweet key={tweet.id} username={tweet.username} content={tweet.content} />
            ))}
        </div>
    );
};

export default Home;
