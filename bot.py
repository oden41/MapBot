#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import sys
import urllib
import urllib2
import cStringIO
import Image
from textwrap import TextWrapper
from datetime import datetime

consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""
USER = "@"
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class StreamWatcherListener(tweepy.StreamListener):

	status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

	def on_status(self, status):
		try:
			mainText = self.status_wrapper.fill(status.text).replace(USER, "").replace(" ", "")
			print mainText
			getPic(mainText)
			api.update_with_media(status="@" + status.author.screen_name, filename="./test.png", in_reply_to_status_id=status.id)

		except Exception, e:
			print "error in on_status:%s" % e
			pass

	def on_error(self, status_code):
		print 'An error has occured! Status code = %s' % status_code
		return True  # keep stream alive

	def on_timeout(self):
		print 'Snoozing Zzzzzz'
		return True



def getPic(place, zoom=12, imgsize="600x400",
		imgformat="png", maptype="roadmap"):

	try:
		# assemble the URL
		request = "http://maps.google.com/maps/api/staticmap?"  # base URL, append query params, separated by &
		request += "center=%s&" % urllib2.quote(place.encode("utf-8"))
		request += "size=%s&" % imgsize  # tuple of ints, up to 640 by 640
		request += "format=%s&" % imgformat
		request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain
		request += "sensor=false&"   # must be given, deals with getting loction from mobile device 
		print request

		web_sock = urllib.urlopen(request)
		imgdata = cStringIO.StringIO(web_sock.read()) # constructs a StringIO holding the image
		try:
			PIL_img = Image.open(imgdata)
			PIL_img.save('test.png') # save as jpeg
			#return PIL_img
			#PIL_img.show()
		# if this cannot be read as image that, it's probably an error from the server,
		except IOError:
			print "IOError:", imgdata.read() # print error (or it may return a image showing the error"
	except Exception, e:
		print "error in getPic:%s" % e
		sys.exit(1)


def main():
	#API取得
	api.update_status("bot起動[" + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "]")
	stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)
	follow_list = None
	track_list = [USER]
	stream.filter(follow_list, track_list)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		api.update_status("bot停止[" + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "]")
