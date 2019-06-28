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

@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bigml"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("Jacksonville, Fl")
    return render_template("home.html", articles=feed['entries'], weather=weather)

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid="
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        {"description" : parsed["weather"][0]["description"],
         "temperature" : parsed["main"]["temp"],
         "city" : parsed["name"]}
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)
