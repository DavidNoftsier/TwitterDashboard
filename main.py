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
import write_and_read_objects
import user_and_tweet_info
import interface

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
	access_api = False 
	# Switch between using GUI or not
 	use_gui = True 

	if (access_api == False): # Access the stored tweet objects instead of API
		if(use_gui == True): # Start the GUI and access the tweet_objects.txt file
        		interface.start_interface(api, access_api)
		else: # Just access the stored tweet objects
			tweet_object_list = write_and_read_objects.read_json_file()
			non_gui_testing(tweet_object_list)	
	
	else: # Access the API, generate tweet_objects.txt
		if(use_gui == True): # Start the GUI
        		interface.start_interface(api, access_api)
		else:
			# Just access the API
			user_name = 'gavinfree'
        		tweet_object_list = write_and_read_objects. write_tweet_objects_to_file(api, user_name)
        		non_gui_testing(tweet_object_list)	

def non_gui_testing(tweet_object_list):

	user_and_tweet_info.show_user_info(tweet_object_list)
	user_and_tweet_info.show_tweet_info(tweet_object_list)
	user_and_tweet_info.show_users_retweeted_most(tweet_object_list)

if __name__ == '__main__':
	main()
