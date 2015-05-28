'''
Application: Twitter Dashboard 
Author:      David Noftsier

main.py performs serves as the typical main for the Twitter Dashboard application
'''

import tweepy
import imp
import sys
import json
import auth_keys
import basic_and_general_info
import write_and_read_objects
import users_retweeted_most

# utf check
imp.reload(sys)
sys.setdefaultencoding("utf-8")


# Private keys
consumer_key = auth_keys.get_consumer_key()
consumer_secret = auth_keys.get_consumer_secret()
access_token_key = auth_keys.get_access_token_key()
access_token_secret = auth_keys.get_access_token_secret()

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

# Creation of the api, using authentication
api = tweepy.API(auth)

def main():
	
   # Switch between accessing the API or accessing the text file
	offlineMode = True
	# Switch between and using GUI or not
 	useGUI = False 
	
	if (offlineMode == True): # Access the stored tweet objects instead of API
		if(useGUI == True):	# Start the GUI and access the tweet_objects.txt file
			pass
         #interface.createGUI() # NEEDS INTERFACE
		else: # Just access the stored tweet objects
			tweet_object_list = write_and_read_objects.readJsonFile()
			nonGuiTesting(tweet_object_list)	
	
	else: # Access the API, generate tweet_objects.txt
		if(useGUI == True): # Start the GUI
			pass
         #interface.createGUI() # NEEDS INTERFACE
		else:
			# Just access the API
			username = 'gavinfree'
        		tweet_object_list = write_and_read_objects.writeTweetObjectsToFile(api, username)
        		nonGuiTesting(tweet_object_list)	


def getUserData(username, window):
	print(username)

	# Storing a list of statuses
	'''
	tweetStatuses = []
	count = 0
	for tweet in tweet_object_list:
		tweetStatuses.append(tweet['text'])
		count += 1
		if count > 99:
  			break
	'''

	# This generates the 'tweet_objects.txt' and returns tweet_object_list
	#tweet_object_list = write_and_read_objects.writeTweetObjectsToFile(api, username)

	# Only used for testing (when you have previously generated 'tweet_objects.txt' don't exceed your access limit)
	#tweet_object_list = write_and_read_objects.readJsonFile()

	# Example for getting the statuses of tweet objects
	#for tweet in tweet_object_list:
	#print tweet["text"]
	#pass

	#basic_and_general_info.showBasicInfo(tweet_object_list)
	#basic_and_general_info.showGeneralInfo(tweet_object_list)

	#users_retweeted_most.showUsersRetweetedMost(tweet_object_list)

 
	#sent.getSentiment(tweetStatuses, window)
	#for user in tweepy.Cursor(api.followers, screen_name = username).items():
		#print user.screen_name


def nonGuiTesting(tweet_object_list):

	basic_and_general_info.showBasicInfo(tweet_object_list)
	basic_and_general_info.showGeneralInfo(tweet_object_list)

	users_retweeted_most.showUsersRetweetedMost(tweet_object_list)
	pass



if __name__ == '__main__':
	main()
