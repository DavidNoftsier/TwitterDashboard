'''
Application: Twitter Dashboard 
Author:      David Noftsier

user_and_tweet_info.py has two methods. 
show_user_info provides basic information about the user such as name, location and account age.
show_tweet_info provides information about the users' tweets such as average number of daily 
tweets, which of their tweet was retweeted the most and which URLS they used the most. 
show_users_retweeted_most shows which users our target user retweeted the most frequently.
'''

import json
from datetime import datetime
import collections
from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import Tkinter

def show_user_info(tweet_object_list, canvas):

	canvas.create_text(150, 50, anchor='w', text="Account Info", font=("Helvetica", 26)) 
	# Name of the account owner 
	canvas.create_text(150, 70, anchor='w', text='Name: ' + tweet_object_list[0]['user']['name'], font=("Helvetica", 20)) 
	# Screen name 
	canvas.create_text(150, 90, anchor='w', text='Screen Name: ' + tweet_object_list[0]['user']['screen_name'], font=("Helvetica", 20)) 
	# Numeric id of the account
	canvas.create_text(150, 110, anchor='w', text='User ID: ' + tweet_object_list[0]['user']['id_str'], font=("Helvetica", 20))
	# Users location # This requires decoding
	canvas.create_text(150, 130, anchor='w', text='Location: ' + tweet_object_list[0]['user']['location'], font=("Helvetica", 20)) 

	#print 'Account Creation: ' + tweet_object_list[0]['user']['created_at']   # Date the account was created in twitter datetime format

	# Converting from twitter datetime format to python datetime format
	account_creation = datetime.strptime(tweet_object_list[0]['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
	canvas.create_text(150, 150, anchor='w', text='Account Creation: {:%m-%d-%Y}'.format(account_creation), font=("Helvetica", 20)) 

	age = (datetime.now() - account_creation).days        # Account Age in days
	canvas.create_text(150, 170, anchor='w', text='Account Age: ' + str(age / 365) + ' Years, ' + str(age % 365) + ' days', font=("Helvetica", 20)) 

def show_tweet_info(tweet_object_list, canvas):

	account_creation = datetime.strptime(tweet_object_list[0]['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
	age = (datetime.now() - account_creation).days        # Account Age in days
 

  	canvas.create_text(525, 50, anchor='w', text='Tweet Information', font=("Helvetica", 26))
 	# Total number of tweets
 	canvas.create_text(525, 70, anchor='w', text='Total Tweets: ' + str(tweet_object_list[0]['user']['statuses_count']), font=("Helvetica", 20))
 	# Average number of tweets each day 
	canvas.create_text(525, 90, anchor='w', text='Average Number of Tweets Daily: ' + str('%.2f'%(float(tweet_object_list[0]['user']['statuses_count']) / float(age))) , font=("Helvetica", 20))   

	retweet_count = 0
	most_retweeted = 'foo_status' 

	hashtags = []

	urls = []

	count = 0
	for tweet in tweet_object_list:

		# Stores the tweet with the highest amount of retweets 
		if retweet_count < tweet_object_list[count]['retweet_count'] and tweet_object_list[count]['text'].split(' ', 1)[0] != 'RT':
			most_retweeted = tweet_object_list[count]['text']
			retweet_count = tweet_object_list[count]['retweet_count']
 
		# NOTE: str(tweet_object_list[count]['retweeted']) returns true if the API user has retweeted this particular tweet
		# not if the tweet itself is a retweet.

		# Stores the hashtags in a list
		# Only applies if the user is the creator of the tweet
		each_hashtag = 0
		while each_hashtag < len(tweet_object_list[count]['entities']['hashtags']) and tweet_object_list[count]['text'].split(' ', 1)[0] != 'RT': 
			hashtags.append(tweet_object_list[count]['entities']['hashtags'][each_hashtag]['text'])
			each_hashtag+=1
	
		# Stores the urls in a list
		temp_string = ''
		truncated_url = ''
		each_url = 0
		while each_url < len(tweet_object_list[count]['entities']['urls']):
			temp_string = str(tweet_object_list[count]['entities']['urls'][each_url]['expanded_url'].partition('/')[2:3:2]) 
			slash_count = 0
			for i in range(0, len(temp_string)):
				if slash_count > 1:
					break
				if slash_count == 1:
					truncated_url = truncated_url + temp_string[i]
				if temp_string[i] == '/' or (i + 1 < len(temp_string) and slash_count == 1 and (temp_string[i + 1] == '/' or temp_string[i + 1] == '\'')):
					slash_count+=1
			urls.append(truncated_url)
			each_url+=1

		count+=1

	canvas.create_text(525, 170, anchor='w', width=470, text='Most Retweeted Tweet: ' + most_retweeted, font=("Helvetica", 20))   
	canvas.create_text(525, 250, anchor='w', text='Retweet Count for Most Retweeted Tweet : ' + str(retweet_count), font=("Helvetica", 20)) 
 
	top_five_hashtags =  collections.Counter(hashtags).most_common(5)
	canvas.create_text(150, 210, anchor='w', text='Top Five Hashtags Used ', font=("Helvetica", 24)) 
	count = 0
	for hashtag, occurrences in top_five_hashtags:
		canvas.create_text(150, 230+(count*20), anchor='w', text='%s' %hashtag, font=("Helvetica", 20))
		count+=1
	# Include number of occurrences? 
	#for hashtag,occurrences in top_five_hashtags:
		#print "%s is used %s times" %(hashtag,occurences)
 
	top_five_urls =  collections.Counter(urls).most_common(5)
	canvas.create_text(150, 350, anchor='w', text='Top Five Websites Referenced ', font=("Helvetica", 24)) 
	count = 0
	for url, occurrences in top_five_urls:
		canvas.create_text(150, 370+(count*20), anchor='w', text='%s' %url, font=("Helvetica", 20))
		count+=1 
	# Include number of occurrences? 
	#for url,occurrences in top_five_hashtags:
		#print "%s is used %s times" %(url,occurrences)

def show_users_retweeted_most(tweet_object_list, canvas):

    retweets = []
    retweetees = [] 
    count = 0

    # Store retweets in a list
    for tweet in tweet_object_list:
        if tweet_object_list[count]['text'].split(' ', 1)[0] == 'RT':
            retweets.append(tweet_object_list[count]['text'])
        count+=1

    count = 0
    # Store the original tweeters in a list 
    for tweet in retweets:
        temp_string = ''
        retweetee = ''
        temp_string = retweets[count]
        at_and_colon_count = 0
        for i in range(0, len(temp_string)):
            if at_and_colon_count > 1:
                break
            if at_and_colon_count == 1:
                retweetee = retweetee + temp_string[i]
            if temp_string[i] == '@' or (i + 1 < len(temp_string) and (temp_string[i + 1] == ':')):
            #if temp_string[i] == '@' or temp_string[i + 1] == ':': 
                at_and_colon_count+=1
        retweetees.append(retweetee)
        count+=1   

    top_five_retweetees =  collections.Counter(retweetees).most_common(5)
    canvas.create_text(150, 490, anchor='w', text='Top Five Users Most Often Retweeted', font=("Helvetica", 24)) 
    count = 0
    for user, occurrences in top_five_retweetees:
        canvas.create_text(150, 510+(count*20), anchor='w', text='%s' %user, font=("Helvetica", 20)) 
        count+=1
    # Include number of occurrences? 
    #for hashtag,occurrences in top_five_hashtags:
        # print "%s is used %s times" %(hashtag,occurences)
