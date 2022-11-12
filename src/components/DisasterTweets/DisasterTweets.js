import { useEffect, useRef, useState } from 'react';
import * as React from 'react';
import './DisasterTweets.scss';
import axios from 'axios';
// import unknown.png from assets

function DisasterTweets() {

    const [tweet, setTweet] = useState('');
    const onTweetChange = (e) => {
        setTweet(e.target.value);
    }
    
    const [location, setLocation] = useState('');

    const onLocationChange = (e) => {
        setLocation(e.target.value);
    }
    
    const [tweets, setTweets] = useState([]);

    const handleTweet = (e) => {
        e?.preventDefault();
  
        axios.post('http://localhost:5000/tweet_results',{
            text: tweet,
            location: location
       }).then(res => {
            setTweet("")
            setLocation("")
            console.log(res)
            console.log(res.data)  
            setTweets(oldTweets => {
                //add new tweet to the beginning of the array
                const newTweets = [res.data, ...oldTweets];
                //replace tweets in local storage with new tweets
                localStorage.setItem('tweets', JSON.stringify(newTweets));
                return newTweets;
            });
       }).catch(err => {
          console.log(err)
        })

        console.log(tweets);
    }

    const loadTweets = () => {
        // load tweets from local storage
        const tweets = localStorage.getItem('tweets');
        if (tweets) {
            setTweets(JSON.parse(tweets));
        }
    }

    const clearTweets = () => {
        localStorage.setItem('tweets', JSON.stringify([]));
        setTweets([]);
    }

    useEffect(() => {
        loadTweets();
    }, []);
    

    return <div className='DisasterTweets' id='DisasterTweets'>
        <div className="inner">
            <div className="upper">
                <img className="profile__pic" src="https://media.idownloadblog.com/wp-content/uploads/2017/03/Twitter-new-2017-avatar-001.png"/>
                <div className="input__container">
                    <input id="tweet" placeholder="What's Happening?" value={tweet} onChange={onTweetChange}></input>
                    <span className="location__container">
                        <span className="material-symbols-outlined">
                            location_on
                        </span>
                        <input id="location" placeholder="Where?" value={location} onChange={onLocationChange}></input>
                    </span>
                    
                </div>
            </div>
            {/* <div className="right">
                <div className="input__container">
                    <input placeholder="What's Happening?"></input>
                </div>
            </div> */}
            <div className="button__container">
                <button className="tweet__button"  onClick={handleTweet}>Tweet</button>
            </div>
        </div>
        { tweets.map((twt, index) => {
                return <div className="inner past__tweet">
                    <div className="upper">
                        <img className="profile__pic" src="https://media.idownloadblog.com/wp-content/uploads/2017/03/Twitter-new-2017-avatar-001.png"/>
                        <div className="input__container">                    
                            <div readonly className='tweet__div' id="tweet">{twt.tweet}</div>
                            
                            {   twt.location &&
                                <span className="location__container">
                                <span className="material-symbols-outlined">
                                    location_on
                                </span>
                                <input readonly id="location" value={twt.location}></input>
                            </span>
                            }
                            
                        </div>
                    </div>
                    <div className="distaster__status__container">
                        {twt.isDisaster ? 'This is a disaster.' : 'This is not a disaster.'}
                    </div>
                </div>
        })}
        <div className="clear__tweets__container">
            <button className="clear__tweets__button" onClick={clearTweets}>
                Clear Tweets
            </button>
        </div>
    </div>
}

export default DisasterTweets;