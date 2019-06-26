"""
Docstring: RSS Feed webapp
"""
import feedparser
from flask import Flask
from flask import render_template
from flask import request

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
    return render_template("home.html", articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
