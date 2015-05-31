from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import Tkinter
import tweepy
import write_and_read_objects
import user_and_tweet_info_interface

def start_interface(api, access_api):
	app = Tk()
	app.title("Twitter Dashboard")
	canvas = Canvas(app, bg='white')
	search_page(app, api, access_api, canvas)

def search_page(app, api, access_api, canvas):
	# Clear the canvas
	canvas.delete("all")

   	# Loading background image
	search_background = PhotoImage(file="search_background.gif")
	# Set window size based on background image dimensions
	width = search_background.width()
	height = search_background.height()
	app.geometry("%dx%d+0+0" % (width, height))

	# Creating a canvas object to build widgets on
	canvas.pack(expand=YES, fill=BOTH)
	canvas.create_image(0, 0, image=search_background, anchor=NW)
	canvas.create_text(width/2, 120, text="Twitter Dashboard", font=("Helvetica", 46)) 
	canvas.create_text((width/2)-100, 300, text="User Name", font=("Helvetica", 20))

	user_name = StringVar(None)
	user_name_entry = Entry(canvas, textvariable=user_name)
	canvas.create_window((width/2)+30, 300, width=140, height=30, window=user_name_entry)

	if access_api == True:
		search_button = Button(canvas, text="Go!", command= lambda: search_online(api, access_api, user_name_entry, app, canvas, search_background, width, height))
	elif access_api == False:
		search_button = Button(canvas, text="Go!", command= lambda: search_offline(api, access_api, app, canvas, search_background, width, height))
	
	canvas.create_window((width/2)+130, 300, width=50, height=25, window=search_button)

	app.mainloop()

def search_offline(api, access_api, app, canvas, search_background, width, height):

	# Clearing and recreating the canvas
	canvas.delete("all")

	app.geometry("%dx%d+0+0" % (width, height))

	canvas.pack(expand=YES, fill=BOTH)
	canvas.create_image(0, 0, image=search_background, anchor=NW)

	# Get list of tweet objects from existing file
	tweet_object_list = write_and_read_objects.read_json_file()

	# Show all tweet info
	user_and_tweet_info_interface.show_user_info(tweet_object_list, canvas)
	user_and_tweet_info_interface.show_tweet_info(tweet_object_list, canvas)
	user_and_tweet_info_interface.show_users_retweeted_most(tweet_object_list, canvas)

   	# Return to the search screen
	return_button = Button(canvas, text="Search Again", command= lambda: search_page(app, api, access_api, canvas))
	canvas.create_window(800, 650, width=150, height=25, window=return_button)

	app.mainloop()

def search_online(api, access_api, user_name_entry, app, canvas, search_background, width, height):
	# Clearing and recreating the canvas
	canvas.delete("all")

	app.geometry("%dx%d+0+0" % (width, height))

	canvas.pack(expand=YES, fill=BOTH)
	canvas.create_image(0, 0, image=search_background, anchor=NW)

	# Get list of tweet objects from existing file
	tweet_object_list = write_and_read_objects.write_tweet_objects_to_file(api, user_name_entry.get())

	# Show all tweet info
	user_and_tweet_info_interface.show_user_info(tweet_object_list, canvas)
	user_and_tweet_info_interface.show_tweet_info(tweet_object_list, canvas)
	user_and_tweet_info_interface.show_users_retweeted_most(tweet_object_list, canvas)

   	# Return to the search screen
	return_button = Button(canvas, text="Search Again", command= lambda: search_page(app, api, access_api, canvas))
	canvas.create_window(800, 650, width=150, height=25, window=return_button)
	
	app.mainloop()
