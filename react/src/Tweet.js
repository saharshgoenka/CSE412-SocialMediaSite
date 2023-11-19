// Tweet.js

import React from 'react';

const Tweet = ({ username, displayName, content, timestamp, profilePictureUrl, tweetPictureUrl, onReshare }) => {
    const handleReshare = () => {
        if (onReshare) {
            onReshare();
        }
    };

    return (
        <div className="border p-4 my-4 rounded-md bg-gray-700 text-white shadow-md">
            <div className="flex items-center">
                <img
                    src={profilePictureUrl}
                    alt="Profile"
                    className="w-8 h-8 rounded-full mr-2"
                />
                <span className="font-bold text-lg">{username}</span>
                {displayName && (
                    <span className="ml-2 text-gray-400">({displayName})</span>
                )}
            </div>
            <p className="mt-2 text-gray-300">{content}</p>
            {tweetPictureUrl && (
                <div className="flex justify-center mt-2">
                    <img
                        src={tweetPictureUrl}
                        alt="Tweet"
                        className="rounded-md"
                        style={{ maxWidth: '100%', maxHeight: '300px' }} // Adjust the styling as needed
                    />
                </div>
            )}
            <div className="text-gray-500 mt-2">{new Date(timestamp).toLocaleString()}</div>
            <button className="mt-2 p-2 bg-blue-500 text-white rounded" onClick={handleReshare}>
                Reshare
            </button>
        </div>
    );
};

export default Tweet;
