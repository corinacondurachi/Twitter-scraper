import pymongo 
import twython 
import csv
import time
import requests
import datetime


class twitterminer():
    
    twitter_keys = {
        'consumer_key':"",
        'consumer_secret':"",
        'access_token_key':"",
        'access_token_secret':""
    }

    client = pymongo.MongoClient('mongodb://localhost:27017/')

    db = client['twitter_db']
    collection = db['twitter-collection']
    collection2 = db['queue']
    collectioni = db['queue2']

    result1 = db.queue.create_index([('name', pymongo.ASCENDING)], unique=True)
    result2 = db.inter.create_index([('name', pymongo.ASCENDING)], unique=True)

    def __init__(self):
        
        CONSUMER_KEY =self.twitter_keys['consumer_key']
        CONSUMER_SECRET = self.twitter_keys['consumer_secret']
        ACCESS_TOKEN = self.twitter_keys['access_token_key']
        ACCESS_TOKEN_SECRET = self.twitter_keys['access_token_secret']
        self.twitter = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


    def extract_followers(self,user,followers_no):
        
        no_max=200
        c=int(followers_no/no_max)
        r=followers_no-c*no_max
        next_cursor=-1
        for k in range(0,c): 
            try: 
                followers = self.twitter.get_followers_list(cursor=next_cursor,screen_name=user,skip_status=True, include_user_entities=False,count=no_max)
                time.sleep(61)
                next_cursor=followers["next_cursor"]
                # print(len(followers["users"]))
                for i in range (0,no_max):
                    Follower={}
                    Follower = {                                     
                        'name': followers["users"][i]['screen_name']                           
                            }

                    try:
                        y = twitterminer.db.queue.insert_one(Follower) 
                        y = twitterminer.db.inter.insert_one(Follower)
                    except pymongo.errors.DuplicateKeyError:
                        continue 

            except twython.exceptions.TwythonAuthError:
                return
                
        try:       
            followers = self.twitter.get_followers_list(cursor=next_cursor,screen_name=user,skip_status=True, include_user_entities=False,count=r)
            time.sleep(61)
    #         print(len(followers["users"]))
            if r!=len(followers["users"]):
                r=len(followers["users"])
            # print(r)
            for i in range (0, r):
                    Follower={}
                    Follower = {
                        'name':followers["users"][i]['screen_name']                           
                        }
                    # print(followers["users"][i]['screen_name'])
                    # print(Follower)
                    try:
                        y = twitterminer.db.queue.insert_one(Follower)
                        y = twitterminer.db.inter.insert_one(Follower) 
    
                    except pymongo.errors.DuplicateKeyError:
                        continue
        except twython.exceptions.TwythonAuthError:
            return
            
    def extract_user_data(self, user=" set default user to get data from"):

        try:
            statuses = self.twitter.show_user(screen_name=user)    
        except twython.exceptions.TwythonError:
            return


        x = {
                    'id':statuses['id_str'],
                    'type':'username',
                    'value':user,
                    'time': datetime.datetime.now()
                    
                }

        info={}
        info['id']=statuses['id_str']
        info['username']=user

        twitterminer.db.users_data.insert_one(x)

        x = {
                    'id':statuses['id_str'],
                    'type':'screen_name',
                    'value':statuses['screen_name'],
                    'time': datetime.datetime.now()
                }

        info['screen_name']=statuses['screen_name']
        twitterminer.db.users_data.insert_one(x)

        if statuses['location']!='':
           
            x = {
                    'id':statuses['id_str'],
                    'type':'location',
                    'value':statuses['location'],
                    'time': datetime.datetime.now()
                }

            info['location']=statuses['location']
            twitterminer.db.users_data.insert_one(x)

        if statuses['description']!='':
            
            x = {
                    'id':statuses['id_str'],
                    'type':'description',
                    'value':statuses['description'],
                    'time': datetime.datetime.now()
                }

            info['description']=statuses['description']
            twitterminer.db.users_data.insert_one(x)

        

        if len(statuses['entities'])>1:
            x = {
        			'id':statuses['id_str'],
                    'type':'URL',
                    'value':statuses['entities']['url']['urls'][0]['expanded_url'],
                    'time': datetime.datetime.now()
        		}

            info['URL']=statuses['entities']['url']['urls'][0]['expanded_url']
            twitterminer.db.users_data.insert_one(x)        
        
        return info

    def extract_tweets_by_geolocation(self,latitude, longitude, max_range) :

        mylist=[]
        tweets=self.twitter.search(count=200, geocode = "%f,%f,%dkm" % (latitude, longitude, max_range))

        for i in range(0,len(tweets['statuses'])):
            mylist.append(tweets['statuses'][i]['created_at'])
            mylist.append(tweets['statuses'][i]['id'])
            mylist.append(tweets['statuses'][i]['text'])
            mylist.append(tweets['statuses'][i]['geo'])
            mylist.append(tweets['statuses'][i]['place'])
            mylist.append(tweets['statuses'][i]['coordinates'])
    
        return mylist
    

    def extract_locations_of_a_user(self,username) :

        mylist=[]
        tweets = self.twitter.get_user_timeline(screen_name=username,count=200)

        for i in range(len(tweets)):
            if tweets[i]['place']!=None:
                mylist.append(tweets[i]['user']['screen_name'])
                mylist.append(tweets[i]['id'])
                mylist.append(tweets[i]['place']['full_name'])
                mylist.append(tweets[i]['place']['bounding_box'])

        return mylist


    def extract_users_inter_collection (self):
        for x in twitterminer.db.inter.find():
            self.extract_user_data(x['name'])
            twitterminer.db.inter.delete_one(x)  


    def initialize(self):
        twitterminer.db.queue.delete_many({})
        twitterminer.db.users_data.delete_many({}) 
        twitterminer.db.inter.delete_many({})
        user= "dragomihailov"        
        self.extract_user_data(user) 
        x= twitterminer.db.users_data.find_one()
        statuses   = self.twitter.show_user(screen_name=user)
        no_followers=statuses['followers_count']
        self.extract_followers(user, no_followers)


        

# x=extract_location("jachymc")
# print(x)
# x=extract_tweets_by_geolocation(44.439663,26.096306,10)




       
    



