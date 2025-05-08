import json

class TweetDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.tweets = []

    def insert_tweet(self, tweet_data):
        self.tweets.append(tweet_data)

    def export_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.tweets, f, ensure_ascii=False, indent=4)

    def print_all_tweets(self):
        for tweet in self.tweets:
            print(tweet)
    
    def close(self):
        pass
