from flask import Flask, render_template, jsonify, request, send_from_directory
import requests
import json
import os
from datetime import datetime, timedelta
import time
from textblob import TextBlob
import feedparser
from urllib.parse import quote
import statistics
import csv
import io

app = Flask(__name__)

# Configuration
NBA_API_KEY = "f2b0dbffbed147ad9c2a2ea050b7274c"
YOUTUBE_API_KEY = "AIzaSyAbTk3dh42inDAQZ7-OYsWXiMRfLcbCKmM"

@app.route('/')
def index():
    """Main page of the Telegram Web App"""
    return render_template('index.html')

@app.route('/nba-analysis')
def nba_analysis():
    """NBA Analysis page"""
    return render_template('nba_analysis.html')

@app.route('/sentiment-analysis')
def sentiment_analysis():
    """Sentiment Analysis page"""
    return render_template('sentiment_analysis.html')

@app.route('/video-highlights')
def video_highlights():
    """Video Highlights page"""
    return render_template('video_highlights.html')

@app.route('/api/nba-games')
def get_nba_games():
    """API endpoint to fetch NBA games data"""
    try:
        # Get recent games from the last 7 days
        games_data = []
        
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDateFinal/{date}"
            params = {"key": NBA_API_KEY}
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                daily_games = response.json()
                for game in daily_games[:5]:  # Limit to 5 games per day
                    games_data.append({
                        'date': date,
                        'home_team': game.get('HomeTeam', 'Unknown'),
                        'away_team': game.get('AwayTeam', 'Unknown'),
                        'home_score': game.get('HomeTeamScore', 0),
                        'away_score': game.get('AwayTeamScore', 0),
                        'status': game.get('Status', 'Unknown'),
                        'point_spread': game.get('PointSpread', 'N/A')
                    })
            
            if len(games_data) >= 20:  # Limit total games
                break
            
            time.sleep(1)  # Rate limiting
        
        return jsonify({
            'success': True,
            'games': games_data,
            'total': len(games_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/predict-game', methods=['POST'])
def predict_game():
    """API endpoint to predict game outcome"""
    try:
        data = request.get_json()
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        point_spread = float(data.get('point_spread', 0))
        home_moneyline = float(data.get('home_moneyline', 0))
        away_moneyline = float(data.get('away_moneyline', 0))
        
        # Simple prediction logic based on betting odds
        if home_moneyline < away_moneyline:
            predicted_winner = home_team
            confidence = min(0.8, abs(away_moneyline - home_moneyline) / 200)
        else:
            predicted_winner = away_team
            confidence = min(0.8, abs(home_moneyline - away_moneyline) / 200)
        
        # Adjust based on point spread
        if abs(point_spread) > 7:
            confidence += 0.1
        
        confidence = min(0.95, max(0.55, confidence))
        
        return jsonify({
            'success': True,
            'prediction': {
                'predicted_winner': predicted_winner,
                'confidence': round(confidence, 2),
                'point_spread': point_spread,
                'analysis': f"Based on moneylines and spread, {predicted_winner} has a {confidence*100:.0f}% chance of winning."
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/lakers-sentiment')
def get_lakers_sentiment():
    """API endpoint to analyze Lakers sentiment from social media"""
    try:
        posts = []
        
        # Get Reddit posts via RSS
        reddit_sources = [
            ('lakers', 'lakers'),
            ('nba', 'lakers'),
            ('basketball', 'lakers')
        ]
        
        for subreddit, query in reddit_sources:
            try:
                search_url = f"https://www.reddit.com/r/{subreddit}/search.rss?q={quote(query)}&restrict_sr=1&sort=new&limit=5"
                response = requests.get(search_url, headers={'User-Agent': 'Lakers-Sentiment-Bot/1.0'}, timeout=10)
                
                if response.status_code == 200:
                    feed = feedparser.parse(response.content)
                    for entry in feed.entries[:3]:
                        if 'lakers' in entry.title.lower():
                            posts.append({
                                'source': f'Reddit r/{subreddit}',
                                'title': entry.title,
                                'content': entry.summary[:200] + "..." if len(entry.summary) > 200 else entry.summary,
                                'date': entry.published,
                                'url': entry.link
                            })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error fetching from r/{subreddit}: {e}")
        
        # Analyze sentiment
        analyzed_posts = []
        sentiment_scores = []
        
        for post in posts[:10]:  # Limit to 10 posts
            full_text = f"{post['title']} {post['content']}"
            
            try:
                blob = TextBlob(full_text)
                polarity = blob.sentiment.polarity
                
                if polarity > 0.1:
                    sentiment_label = "positive"
                elif polarity < -0.1:
                    sentiment_label = "negative"
                else:
                    sentiment_label = "neutral"
                
                post['sentiment_score'] = polarity
                post['sentiment_label'] = sentiment_label
                analyzed_posts.append(post)
                sentiment_scores.append(polarity)
                
            except Exception as e:
                print(f"Error analyzing sentiment: {e}")
        
        # Calculate overall sentiment
        if sentiment_scores:
            avg_sentiment = statistics.mean(sentiment_scores)
            sentiment_counts = {
                'positive': sum(1 for score in sentiment_scores if score > 0.1),
                'negative': sum(1 for score in sentiment_scores if score < -0.1),
                'neutral': sum(1 for score in sentiment_scores if -0.1 <= score <= 0.1)
            }
            
            if avg_sentiment > 0.1:
                overall_sentiment = "positive"
            elif avg_sentiment < -0.1:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"
        else:
            avg_sentiment = 0
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            overall_sentiment = "neutral"
        
        return jsonify({
            'success': True,
            'posts': analyzed_posts,
            'analysis': {
                'average_sentiment': round(avg_sentiment, 3),
                'overall_sentiment': overall_sentiment,
                'sentiment_counts': sentiment_counts,
                'total_posts': len(analyzed_posts)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/youtube-highlights')
def get_youtube_highlights():
    """API endpoint to fetch NBA highlights from YouTube"""
    try:
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'key': YOUTUBE_API_KEY,
            'part': 'snippet',
            'q': 'NBA highlights basketball',
            'type': 'video',
            'order': 'relevance',
            'maxResults': 10,
            'publishedAfter': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'videoDuration': 'short'
        }
        
        response = requests.get(search_url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            videos = []
            
            for item in data.get('items', []):
                video = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:150] + "..." if len(item['snippet']['description']) > 150 else item['snippet']['description'],
                    'channel': item['snippet']['channelTitle'],
                    'published': item['snippet']['publishedAt'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video)
            
            return jsonify({
                'success': True,
                'videos': videos,
                'total': len(videos)
            })
        else:
            return jsonify({
                'success': False,
                'error': f"YouTube API error: {response.status_code}"
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)