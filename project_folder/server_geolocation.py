import flask
import json
import scraper
from bson.json_util import dumps 

ob = scraper.twitterminer()

app = flask.Flask(__name__)

@app.route("/get_tweet/latitude=<latitude>/longitude=<longitude>/max_range=<max_range>")
def get_user(**kwarg):
	try:
	    x=ob.extract_tweets_by_geolocation(float(kwarg['latitude']),float(kwarg['longitude']),int(kwarg['max_range']))
	    y=dumps(x,ensure_ascii=False)
	    return y
	 
	except Exception as e:
	    return dumps({'error' : str(e)})

if __name__ == '__main__':
    app.run(port=9000)

