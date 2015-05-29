'''
Application: Twitter Dashboard 
Author:      David Noftsier

write_and_read_objects.py allows the application developer store tweet objects by accessing the 
Twitter API once, and then makes the tweet objects available for offline testing. This circumvents
the problem of exceeding the Twitter API rate limits.
'''

import tweepy
import json

def write_tweet_objects_to_file(api, user_name): 

	tweet_object_list = []

	# This loop will read either all of a users tweets or 3240 tweets (whichever is reached first) 
	with open('tweet_objects.txt', 'w') as out_file:
		for tweet in tweepy.Cursor(api.user_timeline, screen_name = user_name).items():
			out_file.write(json.dumps(tweet._json) + '\n')
 			tweet_object_list.append(json.loads(json.dumps(tweet._json) + '\n'))  

	return tweet_object_list  

# This is only for reading from the text file - when using the app in real time this will not be called
def read_json_file():

	tweet_object_list = []

	with open('tweet_objects.txt') as file:
		for line in file:
			json_obj = json.loads(line)
			tweet_object_list.append(json_obj)

   # Syntax for accessing attributes
   #print json_obj["text"]
   #print tweet_object_list[0]["text"]
	return tweet_object_list
