import configparser
from tweepy import API, Cursor, OAuthHandler
import pandas as pd

# getting the credentials from config.ini
configs = configparser.ConfigParser()
configs.read('./config.ini')
keys = configs['TWITTER']
consumer_key = keys['CONSUMER_KEY'] 
consumer_secret = keys['CONSUMER_SECRET'] 
access_token = keys['ACCESS_TOKEN']
access_secret = keys['ACCESS_SECRET']

# Authenticating connection to Twitter API using the crendentials
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth, wait_on_rate_limit=True)

#will store the ids of the followers
ids = []
for fid in Cursor(api.get_follower_ids, screen_name='edgeforex1', count=5000).items():
    ids.append(fid)

#info will have all the required informantion of the corresponding ids
info = []
for i in range(0, len(ids), 100):
    try:
        #providing a step values so that we will look up users in chunks
        chunk = ids[i:i+100]
        info.extend(api.lookup_users(user_id=chunk))
    except:
        import traceback
        traceback.print_exc()
        print('Something went wrong, skipping...')

#creating the csv file from the json response stored in info
data = [x._json for x in info]
df = pd.DataFrame(data)
df = df[['id', 'name', 'screen_name', 'location', 'description', 'url', 'followers_count', 'friends_count', 'created_at', 'verified']]
df.to_csv('followers.csv', index=False)