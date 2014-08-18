from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from instagram.client import InstagramAPI
import urllib2
import json
import os

app = Flask(__name__)
Bootstrap(app)
INSTAGRAM_CLIENT_ID = ''
INSTAGRAM_CLIENT_SECRET = ''

api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                   client_secret=INSTAGRAM_CLIENT_SECRET)

@app.route('/')
def pictures():
	recent = api.tag_recent_media(1,100,'philadelphia')
	link = recent[1]
	response = urllib2.urlopen(link)
	ig = json.load(response) 
	status=ig['meta']['code']
	imgs = []
	data = ig['data']

    
	for x in range(100):
			if not data:
				link = ig['pagination']['next_url']
				response = urllib2.urlopen(link)
				ig = json.load(response)
			else:
				image = ig['data'][0]['images']['standard_resolution']['url']
				imgs.append(image)
				link = ig['pagination']['next_url']
				response = urllib2.urlopen(link)
				ig = json.load(response)

	return render_template('index.html', tags=imgs)
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

