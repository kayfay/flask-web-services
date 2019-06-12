"""
Docstring: RSS Feed webapp
"""
import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {'bigml' : "https://blog.bigml.com/feed",
             'googl' : "https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&q=Machine+Learning&output=rss",
             'redit' : "https://www.reddit.com/r/MachineLearning/.rss",
             'mit'   : "http://news.mit.edu/rss/topic/machine-learning"}



@app.route("/")
@app.route("/<publication>")
def get_news(publication="bigml"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return """<html>
      <body>
          <h1> ML Headlines </h1>
          <b><{0}</b> <br />
          <i><{1}</i> <br />
          <p><{2}</p> <br />
      </body>
    </html>""".format(first_article.get("title"),
                      first_article.get("published"),
                      first_article.get("summary"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
