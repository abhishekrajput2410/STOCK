from textblob import TextBlob
import requests

NEWS_API_KEY = "f10d8c429dfb420c88bbd5617067f2bb"

def get_news_sentiment(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    res = requests.get(url).json()

    sentiments = []
    for article in res.get("articles", [])[:10]:
        polarity = TextBlob(article["title"]).sentiment.polarity
        sentiments.append(polarity)

    if not sentiments:
        return "Neutral"

    avg = sum(sentiments) / len(sentiments)

    if avg > 0.1:
        return "Positive"
    elif avg < -0.1:
        return "Negative"
    else:
        return "Neutral"
