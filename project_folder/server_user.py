import flask
import json
import scraper
from bson.json_util import dumps 


ob = scraper.twitterminer()

app = flask.Flask(__name__)

@app.route("/get_user/<name>")
def get_user(**kwarg):
	try:
	    x=ob.db.users_data.find({ 'username' : kwarg['name']})

	    y=dumps(x)
	    if(len(y)>2):
	    	return y
	    else:
	    	x=ob.extract_user_data(kwarg['name'])
	    	y=dumps(x)
	    	return y

	except Exception as e:
	    return dumps({'error' : str(e)})

if __name__ == '__main__':
    app.run(port=9500)



