import scraper

obj = scraper.twitterminer()
# obj.initialize()

while(True):

    obj.extract_users_inter_collection()
    x= obj.db.queue.find_one()
    user=x['name']
    try:
      statuses   =   obj.twitter.show_user(screen_name=user)
      if statuses['followers_count']!=0:
        obj.extract_followers(x['name'], statuses['followers_count'])
      
    except: 
      print("Deleted user")

    x = obj.db.queue.delete_one(x)
