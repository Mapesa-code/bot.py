# NBA Analytics Telegram Web App

A comprehensive NBA analytics web application designed to be used as a Telegram Web App. Features real-time NBA game analysis, Lakers sentiment tracking, and video highlights.

## Features

### 🏀 NBA Game Analysis
- Recent NBA games data
- Game outcome predictions based on betting odds
- Point spread analysis
- Interactive prediction tool

### 😊 Lakers Sentiment Analysis
- Real-time social media sentiment tracking
- Reddit post analysis
- Sentiment scoring and visualization
- Overall sentiment trends

### 🎥 Video Highlights
- Latest NBA highlights from YouTube
- High-quality video thumbnails
- Direct links to YouTube videos
- Share functionality

## Telegram Integration

This app is specifically designed to work as a Telegram Web App:
- Responsive design optimized for mobile
- Telegram theme integration
- Native sharing capabilities
- Seamless user experience within Telegram

## Deployment on Render

### Quick Deploy
1. Fork this repository to your GitHub account
2. Connect your GitHub account to Render
3. Create a new Web Service from your forked repository
4. Render will automatically detect the `render.yaml` configuration

### Manual Deploy
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Python Version**: 3.9.18

### Environment Variables
The following API keys are included in the `render.yaml` file:
- `NBA_API_KEY`: For fetching NBA game data
- `YOUTUBE_API_KEY`: For fetching video highlights

## Setting up as Telegram Web App

1. Create a new bot with @BotFather on Telegram
2. Use `/newapp` to create a new Web App
3. Set the Web App URL to your Render deployment URL
4. Configure the bot menu with `/setmenu`

Example menu setup:
```
games - 📊 NBA Game Analysis
sentiment - 😊 Lakers Sentiment  
highlights - 🎥 Video Highlights
```

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
git clone <your-repo-url>
cd nba-telegram-webapp
pip install -r requirements.txt
```

### Running Locally
```bash
python app.py
```

The app will be available at `http://localhost:5000`

### Testing with Telegram
1. Use ngrok to create a public URL: `ngrok http 5000`
2. Use the ngrok URL as your Telegram Web App URL for testing

## API Endpoints

- `GET /` - Main app interface
- `GET /api/nba-games` - Fetch recent NBA games
- `POST /api/predict-game` - Predict game outcomes
- `GET /api/lakers-sentiment` - Get Lakers sentiment analysis
- `GET /api/youtube-highlights` - Fetch NBA highlights
- `GET /health` - Health check endpoint

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: SportsData.io (NBA data), YouTube Data API v3
- **Sentiment Analysis**: TextBlob
- **Social Media**: Reddit RSS feeds
- **Deployment**: Render
- **Integration**: Telegram Web Apps

## File Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── templates/
│   ├── base.html         # Base template with Telegram integration
│   ├── index.html        # Home page
│   ├── nba_analysis.html # NBA analysis page
│   ├── sentiment_analysis.html # Sentiment analysis page
│   └── video_highlights.html # Video highlights page
├── README.md
└── .gitignore
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes  
4. Test locally
5. Submit a pull request

## License

MIT License - feel free to use and modify as needed.

## Support

For issues or questions:
1. Check the GitHub Issues page
2. Contact via Telegram: @yourusername
3. Email: your.email@example.com

---

Built with ❤️ for NBA fans and Telegram users