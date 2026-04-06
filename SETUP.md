# Epic Games Free Games Monitor - Setup Guide

This script monitors Epic Games' free weekly games and sends you an email every Thursday if new games are available.

## Quick Setup

### Step 1: Create Gmail App Password

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - You must have 2-Factor Authentication enabled first
2. Select **Mail** and **Windows Computer** (or your device)
3. Generate the app password (Google will show a 16-character password)
4. **Copy this password** - you'll need it soon

### Step 2: Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository called `epic-games-monitor`
3. Clone it locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/epic-games-monitor.git
   cd epic-games-monitor
   ```

### Step 3: Add Files to Repository

Copy these files into your repository:
- `epic_games_monitor.py`
- `requirements.txt`
- `.github/workflows/epic-games-monitor.yml`

Then push to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Step 4: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add these three secrets:
   - `GMAIL_ADDRESS`: Your Gmail address (e.g., yourname@gmail.com)
   - `GMAIL_PASSWORD`: The 16-character app password from Step 1
   - `RECIPIENT_EMAIL`: Email to receive notifications (can be same as GMAIL_ADDRESS)

### Step 5: Enable Workflows

1. Go to the **Actions** tab in your repository
2. Click **I understand my workflows, go ahead and enable them**

## How It Works

- **Runs**: Every Thursday at 3 PM UTC (when Epic releases new games)
- **Sends Email**: Only if there are new games you haven't been notified about
- **Remembers**: Keeps track of games you've been notified about in `games_notified.json`

## Manual Testing

To test without waiting for Thursday:

1. Go to the **Actions** tab
2. Click on **Epic Games Free Games Monitor**
3. Click **Run workflow** → **Run workflow** (green button)

## Troubleshooting

### Email Not Sending?
- Check you used an **[app password](https://myaccount.google.com/apppasswords)**, not your regular Gmail password
- Verify 2FA is enabled on your Google account
- Check GitHub Action logs for error messages

### Script Not Running?
- Check the **Actions** tab for failed workflow runs
- Click on a failed run to see error details
- Verify all three secrets are set correctly

### Changes Not Saving?
- The script auto-commits the `games_notified.json` file
- Check GitHub repository settings have **Allow GitHub Actions to create and approve pull requests** enabled (if needed)

## Customization

### Change Run Time
Edit `.github/workflows/epic-games-monitor.yml` line 8:
```yaml
- cron: '0 15 * * 4'  # Hour Minute Day Month DayOfWeek (4 = Thursday)
```
Use [crontab.guru](https://crontab.guru) to calculate your preferred time.

### Run Locally (without GitHub Actions)
```bash
python -m pip install -r requirements.txt
export GMAIL_ADDRESS="your-email@gmail.com"
export GMAIL_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient@gmail.com"
python epic_games_monitor.py
```

## Notes

- Emails are sent in nice HTML format
- First run will notify about current free games
- Subsequent runs only email about newly added games
- GitHub provides 35,000+ minutes/month of free Actions (more than enough for once-weekly runs)

Enjoy getting free games! 🎮
