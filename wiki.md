# Project Summary
The NBA Analytics Telegram Web App is a comprehensive platform designed for basketball enthusiasts, providing real-time analysis of NBA games, sentiment tracking for the Los Angeles Lakers, and access to the latest video highlights. This web application integrates multiple APIs to deliver insights, predictions, and social media sentiment analysis, all accessible through a user-friendly interface optimized for Telegram.

# Project Module Description
- **NBA Game Analysis**: Fetches and analyzes recent NBA games, providing predictions based on betting odds and point spreads.
- **Lakers Sentiment Analysis**: Analyzes social media sentiment regarding the Lakers using Reddit data.
- **Video Highlights**: Displays the latest NBA highlights sourced from YouTube.

# Directory Tree
```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment configuration
└── templates/
    ├── base.html         # Base template with Telegram integration
    ├── index.html        # Home page
    ├── nba_analysis.html  # NBA analysis page
    ├── sentiment_analysis.html # Sentiment analysis page
    └── video_highlights.html # Video highlights page
```

# File Description Inventory
- **app.py**: Contains the main application logic, including routes for game analysis, sentiment analysis, and video highlights.
- **requirements.txt**: Lists the necessary Python packages for the application.
- **render.yaml**: Configuration file for deploying the app on Render.
- **templates/**: Directory containing HTML templates for the web application.

# Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: SportsData.io (NBA data), YouTube Data API v3
- **Sentiment Analysis**: TextBlob
- **Social Media**: Reddit RSS feeds
- **Deployment**: Render
- **Integration**: Telegram Web Apps

# Usage
### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd nba-telegram-webapp
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally
To run the application locally:
```bash
python app.py
```
The app will be available at `http://localhost:5000`.

### Deployment on Render
1. Push to GitHub:
   ```bash
   git remote add origin https://github.com/yourusername/nba-telegram-webapp.git
   git branch -M main
   git push -u origin main
   ```
2. Create a new Web Service on Render, connecting your GitHub repository. Render will auto-detect the `render.yaml` file.

### Setting up as Telegram Web App
1. Create a new bot with @BotFather on Telegram.
2. Use `/newapp` to create a new Web App and set the Render URL as the Web App URL.
