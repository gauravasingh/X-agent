"""
X (Twitter) API handler for fetching posts
"""
import tweepy
from config import (
    X_API_KEY,
    X_API_SECRET, 
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET,
    X_BEARER_TOKEN,
    POSTS_PER_RUN
)
from typing import List, Dict
import json


class XPostFetcher:
    def __init__(self):
        """Initialize X API client"""
        self.client = tweepy.Client(
            bearer_token=X_BEARER_TOKEN,
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
    
    def fetch_trending_posts(self, limit: int = POSTS_PER_RUN) -> List[Dict]:
        """
        Fetch trending posts from X
        
        Args:
            limit: Number of posts to fetch
            
        Returns:
            List of post dictionaries with text, author, engagement metrics
        """
        posts = []
        try:
            # Fetch tweets with high engagement (likes, retweets)
            query = "-is:retweet -is:reply lang:en has:engagement"
            
            tweets = self.client.search_recent_tweets(
                query=query,
                tweet_fields=['public_metrics', 'created_at', 'author_id'],
                user_fields=['username', 'verified', 'followers_count'],
                expansions=['author_id'],
                max_results=min(limit, 100)
            )
            
            if tweets.data:
                users = {user.id: user for user in tweets.includes['users']}
                
                for tweet in tweets.data:
                    author = users.get(tweet.author_id)
                    posts.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'author': author.username if author else 'Unknown',
                        'author_verified': author.verified if author else False,
                        'author_followers': author.followers_count if author else 0,
                        'likes': tweet.public_metrics['like_count'],
                        'retweets': tweet.public_metrics['retweet_count'],
                        'replies': tweet.public_metrics['reply_count'],
                        'quotes': tweet.public_metrics['quote_count']
                    })
        except Exception as e:
            print(f"Error fetching tweets: {e}")
        
        return posts
    
    def fetch_by_keywords(self, keywords: List[str], limit: int = POSTS_PER_RUN) -> List[Dict]:
        """
        Fetch posts by specific keywords
        
        Args:
            keywords: List of keywords to search
            limit: Number of posts per keyword
            
        Returns:
            List of matching posts
        """
        posts = []
        for keyword in keywords:
            try:
                query = f"{keyword} -is:retweet lang:en"
                tweets = self.client.search_recent_tweets(
                    query=query,
                    tweet_fields=['public_metrics', 'created_at', 'author_id'],
                    user_fields=['username', 'verified', 'followers_count'],
                    expansions=['author_id'],
                    max_results=min(limit // len(keywords), 100)
                )
                
                if tweets.data:
                    users = {user.id: user for user in tweets.includes['users']}
                    for tweet in tweets.data:
                        author = users.get(tweet.author_id)
                        posts.append({
                            'keyword': keyword,
                            'id': tweet.id,
                            'text': tweet.text,
                            'created_at': tweet.created_at,
                            'author': author.username if author else 'Unknown',
                            'author_verified': author.verified if author else False,
                            'author_followers': author.followers_count if author else 0,
                            'likes': tweet.public_metrics['like_count'],
                            'retweets': tweet.public_metrics['retweet_count'],
                        })
            except Exception as e:
                print(f"Error fetching tweets for keyword '{keyword}': {e}")
        
        return posts
    
    def save_posts_cache(self, posts: List[Dict], filename: str = "posts_cache.json"):
        """Save fetched posts to cache"""
        with open(filename, 'w') as f:
            json.dump(posts, f, indent=2, default=str)
