"""
Docstring: RSS Feed webapp
"""
import feedparser
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request

import datetime
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


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


@app.route("/")
def home():
    """Renders a homepage Jinija template.

    Uses render_template from flask to create a Jinja template that modfies
    the page based on news and weather functions.
    """
    # get customized headlines based on user input of default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # get customized weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    # save cookies and return template
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_rate(frm, to):
    all_currency = urllib2.urlopen(EXCHANGE_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_news(query):
    feed = feedparser.parse(RSS_FEEDS[publication.lower()])
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
         "temperature" : (9.0/5*parsed["main"]["temp"])+32,
         "city" : parsed["name"],
         "country" : parsed['sys']['country']}
    return weather

if __name__ == "__main__":
    app.run(port=5000, debug=True)
