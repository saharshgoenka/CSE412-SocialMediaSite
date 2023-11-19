// AddTweet.js

import React, { useState } from 'react';

const AddTweet = () => {
    const [tweet, setTweet] = useState('');

    const handleTweetChange = (e) => {
        setTweet(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Add logic to handle the submission of the tweet
        console.log('Tweet submitted:', tweet);
    };

    return (
        <div className="container mx-auto mt-4">
            <form onSubmit={handleSubmit}>
                <label className="block mb-2">Add Tweet:</label>
                <textarea
                    className="border p-2 w-full"
                    rows="4"
                    placeholder="What's happening?"
                    value={tweet}
                    onChange={handleTweetChange}
                ></textarea>
                <button className="bg-blue-500 text-white p-2 mt-2" type="submit">Post Tweet</button>
            </form>
        </div>
    );
};

export default AddTweet;
