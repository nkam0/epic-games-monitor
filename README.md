# Epic Games Free Games Monitor

Automatically monitor Epic Games' free weekly games and get email notifications every Thursday.

## Features

✅ **Automatic Monitoring**: Runs every Thursday at 3 PM UTC  
✅ **Email Alerts**: Receives beautifully formatted emails with game details  
✅ **Smart Tracking**: Only sends emails about new games (remembers what you've been notified of)  
✅ **Free Cloud Hosting**: Runs on GitHub Actions (completely free)  
✅ **No Server Required**: No need to keep your computer on  

## Quick Start

1. **Get Gmail App Password** → https://myaccount.google.com/apppasswords
2. **Create GitHub repository** → https://github.com/new
3. **Add files** from this directory to your GitHub repo
4. **Add 3 secrets** to GitHub (GMAIL_ADDRESS, GMAIL_PASSWORD, RECIPIENT_EMAIL)
5. **Enable workflows** in the Actions tab

See [SETUP.md](SETUP.md) for detailed instructions.

## How to Use

- **Automatic**: Runs every Thursday at 3 PM UTC
- **Manual Test**: Go to Actions → Run workflow
- **Local Testing**: `python epic_games_monitor.py` (with environment variables set)

## Technical Details

- **Language**: Python 3  
- **Dependencies**: `requests` library  
- **Data**: Fetches from Epic Games official API  
- **Storage**: Tracks notified games in `games_notified.json`  
- **Frequency**: Free tier of GitHub Actions (2,000+ runs per month available)

## Files

- `epic_games_monitor.py` - Main script
- `requirements.txt` - Python dependencies
- `.github/workflows/epic-games-monitor.yml` - GitHub Actions workflow
- `SETUP.md` - Detailed setup guide
- `games_notified.json` - Tracks which games you've been notified about (auto-created)

## Support

Having issues? Check [SETUP.md](SETUP.md#troubleshooting) for common solutions.
