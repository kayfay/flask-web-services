"""
Docstring: RSS Feed webapp
"""
import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib
import urllib2

app = Flask(__name__)

RSS_FEEDS = {'bigml' : "https://blog.bigml.com/feed",
             'googl' : "https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&q=Machine+Learning&output=rss",
             'redit' : "https://www.reddit.com/r/MachineLearning/.rss",
             'mit'   : "http://news.mit.edu/rss/topic/machine-learning"}

DEFAULTS = {'publication' : 'bigml',
            'city' : 'Jacksonville, FL'}

API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid="

@app.route("/")
def home():
    """Renders a homepage Jinija template.

    Uses render_template from flask to create a Jinja template that modfies
    the page based on news and weather functions.
    """
    # get customized headlines based on user input of default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        publication = DEFAULTS['city']
    publication = get_weather(city)

    return render_template("home.html", articles=articles, weather=weather)

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.parse.quote(query)
    url = API_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = \
        {"description" : parsed["weather"][0]["description"],
         "temperature" : parsed["main"]["temp"],
         "city" : parsed["name"],
         "country" : parsed['sys']['country']}
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)
