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
            'city' : 'Jacksonville',
            'currency_from' : 'USD',
            'currency_to' : 'INR'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=45da5f9a7db0f15fa1ee596e17cfa2b7"

EXCHANGE_URL = "https://openexchangerates.org//api/latest.json?app_id=0006786932eb42d98798a620fdba059a"

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
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from, currency_to)

    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate)

def get_rate(frm, to):
    all_currency = urllib2.urlopen(EXCHANGE_URL).read()

    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
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
