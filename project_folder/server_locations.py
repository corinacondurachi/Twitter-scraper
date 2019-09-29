import flask
import json
import scraper
from bson.json_util import dumps 

ob = scraper.twitterminer()

app = flask.Flask(__name__)

@app.route("/get_location/<username>")
def get_user(**kwarg):
	try:
	    x=ob.extract_locations_of_a_user((kwarg['username']))
	    y=dumps(x,ensure_ascii=False)
	    return y
	 

	except Exception as e:
	    return dumps({'error' : str(e)})

if __name__ == '__main__':
    app.run(port=8000)









