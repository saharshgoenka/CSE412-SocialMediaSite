// App.js

import React, { useState } from 'react';
import Tweet from './Tweet';

function App() {
    const [showForm, setShowForm] = useState(false);
    const [newTweet, setNewTweet] = useState({
        content: '',
        tweetPictureUrl: '',
    });

    const tweets = [
        {
            id: 1,
            username: 'user1',
            displayName: 'User One',
            content: 'This is my first tweet!',
            timestamp: '2023-11-18T12:30:00',
            profilePictureUrl: 'https://placekitten.com/40/40',
            tweetPictureUrl: 'https://placekitten.com/300/150',
        },
        {
            id: 2,
            username: 'user2',
            displayName: 'User Two',
            content: 'Excited to use my social media site!',
            timestamp: '2023-11-18T13:45:00',
            profilePictureUrl: 'https://placekitten.com/40/41',
            tweetPictureUrl: '',
        },
        {
            id: 3,
            username: 'user3',
            displayName: 'User Three',
            content: 'Just added another tweet to the feed!',
            timestamp: '2023-11-18T15:00:00',
            profilePictureUrl: 'https://placekitten.com/40/42',
            tweetPictureUrl: 'https://placekitten.com/300/200',
        },
        // Add more tweets as needed
    ];

    const handleInputChange = (e) => {
        setNewTweet({ ...newTweet, [e.target.name]: e.target.value });
    };

    const handleAddTweet = () => {
        const newTweetWithTimestamp = {
            ...newTweet,
            id: tweets.length + 1,
            timestamp: new Date().toISOString(),
        };
        setNewTweet({
            content: '',
            tweetPictureUrl: '',
        });
        // Add logic to update the tweets array with the new tweet
        // For example, setTweets([...tweets, newTweetWithTimestamp]);
    };

    const handleReshare = () => {
        console.log('Reshare button clicked');
    };

    return (
        <div className="App text-center bg-gray-800 text-white min-h-screen">
            <div className="container mx-auto py-8">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold">CSE 412 Social Media Site</h1>
                    <button onClick={() => setShowForm(true)} className="bg-blue-500 text-white py-2 px-4 rounded mt-4">
                        Add Tweet
                    </button>
                </header>
                {showForm && (
                    <div className="mt-4">
                        <form className="flex flex-col items-center">
                            <label className="mb-2 text-gray-300">
                                Tweet Content:
                                <textarea
                                    name="content"
                                    value={newTweet.content}
                                    onChange={handleInputChange}
                                    className="border rounded p-2 bg-gray-700 text-white w-full"
                                />
                            </label>
                            <label className="mb-2 text-gray-300">
                                Tweet Picture URL (optional):
                                <input
                                    type="text"
                                    name="tweetPictureUrl"
                                    value={newTweet.tweetPictureUrl}
                                    onChange={handleInputChange}
                                    className="border rounded p-2 bg-gray-700 text-white w-full"
                                />
                            </label>
                            <button type="button" onClick={handleAddTweet}
                                    className="bg-green-500 text-white py-2 px-4 rounded mt-4">
                                Post Tweet!
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
            </div>
        </div>
    );
}

export default App;
