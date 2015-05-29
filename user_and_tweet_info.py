'''
Application: Twitter Dashboard 
Author:      David Noftsier

user_and_tweet_info.py has two methods. 
show_user_info provides basic information about the user such as name, location and account age.
show_tweet_info provides information about the users' tweets such as average number of daily 
tweets, which of their tweet was retweeted the most and which URLS they used the most. 
'''

import json
from datetime import datetime
import collections

def show_user_info(tweet_object_list):

	print 'Name: ' + tweet_object_list[0]['user']['name'] # Name of the account owner
	print 'Screen Name: ' + tweet_object_list[0]['user']['screen_name'] # Screen name 
	print 'User ID: ' + tweet_object_list[0]['user']['id_str'] # Numeric id of the account
	print 'Location: ' + tweet_object_list[0]['user']['location']     # Users location # This requires decoding

	#print 'Account Creation: ' + tweet_object_list[0]['user']['created_at']   # Date the account was created in twitter datetime format

	# Converting from twitter datetime format to python datetime format
	account_creation = datetime.strptime(tweet_object_list[0]['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
	print 'Account Creation: {:%m-%d-%Y}'.format(account_creation) # Formatting

	age = (datetime.now() - account_creation).days        # Account Age in days
	print 'Account Age: ' + str(age / 365) + ' Years, ' + str(age % 365) + ' days'   # Formatting

def show_tweet_info(tweet_object_list):

	account_creation = datetime.strptime(tweet_object_list[0]['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
	age = (datetime.now() - account_creation).days        # Account Age in days
 
	print 'Total Tweets: ' + str(tweet_object_list[0]['user']['statuses_count'])  # Total number of tweets
	print 'Average Number of Tweets Daily: ' + str('%.2f'%(float(tweet_object_list[0]['user']['statuses_count']) / float(age)))   # Average number of tweets each day
 
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

	print 'Most Retweeted Tweet: ' + most_retweeted
	print 'Retweet Count for Most Retweeted Tweet : ' + str(retweet_count)
 
	top_five_hashtags =  collections.Counter(hashtags).most_common(5)
	print 'Top Five Hashtags Used: '
	for hashtag, occurrences in top_five_hashtags:
		print '\t\t\t%s' %hashtag
	# Include number of occurrences? 
	#for hashtag,occurrences in top_five_hashtags:
		#print "%s is used %s times" %(hashtag,occurences)
 
	top_five_urls =  collections.Counter(urls).most_common(5)
	print 'Top Five Websites Referenced: '
	for url, occurrences in top_five_urls:
		print '\t\t\t%s' %url
	# Include number of occurrences? 
	#for url,occurrences in top_five_hashtags:
		#print "%s is used %s times" %(url,occurrences)
