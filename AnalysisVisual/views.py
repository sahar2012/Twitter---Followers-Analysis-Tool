from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

from twython import Twython
import time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import csv

# Create your views here.
def index(request):
	if request.method == 'POST':
		testInputString = str(request.POST['TestInputString'])
		testInputString = testInputString.strip()
		ids = testInputString.split(",")


		t = Twython(app_key=APP_KEY,
	    	app_secret=APP_SECRET,
	    	oauth_token=OUATH TOKEN,
	    	oauth_token_secret=OAUTH TOKEN SECRET)
		followers = []
		next_cursor = -1
		followersDict = dict()
		allNodes = set()
		allNodes.update(ids)

		for tid in ids:
		    followers = []
		    next_cursor = -1
		    while(next_cursor):
		        get_followers = t.get_followers_list(screen_name=tid,count=200,cursor=next_cursor)
		        #time.sleep(20)   #to avoid rate limit exceed error
		        for follower in get_followers["users"]:
		            followers.append(follower["screen_name"].encode("utf-8"))
		            next_cursor = get_followers["next_cursor"]
		    followersDict[tid] = followers
		    allNodes.update(followers)

		
		allFollowerNodes = allNodes - set(ids)
		commonFollowers = set(followersDict[ids[0]])
		for i in range(len(ids)):
			commonFollowers = set(commonFollowers) & set(followersDict[ids[i]])
		print commonFollowers

		with open('AnalysisVisual/static/csvfile.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			writer.writerow(["source", "target", "value"])
			for tid in ids:
				for nodes in followersDict[tid]:
					if nodes in commonFollowers:
						writer.writerow([nodes,tid,"0.2"])
					else: 
						writer.writerow([nodes,tid,"0.8"])

		return render (request,'graph.html')
		

	else:
		return render (request,'index.html')