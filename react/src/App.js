// App.js

import React, { useState } from 'react';
import Tweet from './Tweet';

function App() {
    const [showForm, setShowForm] = useState(false);
    const [newTweet, setNewTweet] = useState({ username: '', displayName: '', content: '', timestamp: '', profilePictureUrl: '', tweetPictureUrl: '' });

    const tweets = [
        {
            id: 1,
            username: 'user1',
            displayName: 'User One',
            content: 'This is my first tweet!',
            timestamp: '2023-11-18T12:30:00',
            profilePictureUrl: 'https://placekitten.com/40/40', // Replace with the actual profile picture URL
            tweetPictureUrl: 'https://placekitten.com/300/150', // Optional tweet picture URL
        },
        {
            id: 2,
            username: 'user2',
            displayName: 'User Two',
            content: 'Excited to use my social media site!',
            timestamp: '2023-11-18T13:45:00',
            profilePictureUrl: 'https://placekitten.com/40/41', // Replace with the actual profile picture URL
            tweetPictureUrl: '', // No optional tweet picture for this tweet
        },
        {
            id: 3,
            username: 'user3',
            displayName: 'User Three',
            content: 'Just added another tweet to the feed!',
            timestamp: '2023-11-18T15:00:00',
            profilePictureUrl: 'https://placekitten.com/40/42', // Replace with the actual profile picture URL
            tweetPictureUrl: 'https://placekitten.com/300/200', // Optional tweet picture URL
        },
        // Add more tweets as needed
    ];

    const handleInputChange = (e) => {
        setNewTweet({ ...newTweet, [e.target.name]: e.target.value });
    };

    const handleAddTweet = () => {
        const newTweetWithTimestamp = { ...newTweet, id: tweets.length + 1, timestamp: new Date().toISOString() };
        setNewTweet({ username: '', displayName: '', content: '', timestamp: '', profilePictureUrl: '', tweetPictureUrl: '' });
        // Add logic to update the tweets array with the new tweet
        // For example, setTweets([...tweets, newTweetWithTimestamp]);
    };

    const handleReshare = () => {
        console.log('Reshare button clicked');
    };

    return (
        <div className="App text-center">
            <header className="App-header">
                <h1 className="text-3xl font-bold mb-4">Twitter Clone</h1>
                <button onClick={() => setShowForm(true)}>Add Tweet</button>
                {showForm && (
                    <div>
                        <form>
                            <label>
                                Username:
                                <input
                                    type="text"
                                    name="username"
                                    value={newTweet.username}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <br />
                            <label>
                                Display Name:
                                <input
                                    type="text"
                                    name="displayName"
                                    value={newTweet.displayName}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <br />
                            <label>
                                Profile Picture URL:
                                <input
                                    type="text"
                                    name="profilePictureUrl"
                                    value={newTweet.profilePictureUrl}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <br />
                            <label>
                                Tweet Picture URL (optional):
                                <input
                                    type="text"
                                    name="tweetPictureUrl"
                                    value={newTweet.tweetPictureUrl}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <br />
                            <label>
                                Tweet Content:
                                <textarea
                                    name="content"
                                    value={newTweet.content}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <br />
                            <button type="button" onClick={handleAddTweet}>
                                Add Tweet
                            </button>
                        </form>
                    </div>
                )}
                {tweets.map((tweet) => (
                    <Tweet
                        key={tweet.id}
                        username={tweet.username}
                        displayName={tweet.displayName}
                        content={tweet.content}
                        timestamp={tweet.timestamp}
                        profilePictureUrl={tweet.profilePictureUrl}
                        tweetPictureUrl={tweet.tweetPictureUrl}
                        onReshare={handleReshare}
                    />
                ))}
            </header>
        </div>
    );
}

export default App;
