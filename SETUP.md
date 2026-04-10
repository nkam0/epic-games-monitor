# Epic Games Free Games Monitor - Setup Guide

This script monitors Epic Games' free weekly games and sends you an email every Thursday if new games are available. It uses [Mailgun](https://www.mailgun.com) to deliver emails via their HTTP API.

## Quick Setup

### Step 1: Create a Mailgun Account

1. Sign up at [mailgun.com](https://www.mailgun.com) (free tier allows 1,000 emails/month)
2. In the Mailgun dashboard, go to **Sending** → **Domains**
3. Add and verify a sending domain (e.g. `mg.yourdomain.com`), or use the sandbox domain for testing
4. Go to **API Keys** (under your account settings) and copy your **Private API key**

You will need:
- **API Key**: starts with `key-...`
- **Sending Domain**: e.g. `mg.yourdomain.com`

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
3. Add these secrets:

| Secret | Description | Example |
|---|---|---|
| `MAILGUN_API_KEY` | Your Mailgun private API key | `key-abc123...` |
| `MAILGUN_DOMAIN` | Your Mailgun sending domain | `mg.yourdomain.com` |
| `MAILGUN_FROM` | Sender address shown in emails | `Epic Games Monitor <noreply@mg.yourdomain.com>` |
| `RECIPIENT_EMAIL` | Email address to receive notifications | `you@example.com` |

> `MAILGUN_FROM` is optional — if omitted, it defaults to `mailgun@{your-domain}`.

### Step 5: Enable Workflows

1. Go to the **Actions** tab in your repository
2. Click **I understand my workflows, go ahead and enable them**

## How It Works

- **Runs**: Every Thursday at 3 PM UTC (when Epic releases new games)
- **Sends Email**: Only if there are new games you haven't been notified about
- **Remembers**: Keeps track of notified games in `games_notified.json`, auto-committed back to the repo

## Manual Testing

To test without waiting for Thursday:

1. Go to the **Actions** tab
2. Click on **Epic Games Free Games Monitor**
3. Click **Run workflow** → **Run workflow** (green button)

## Run Locally

```bash
python -m pip install -r requirements.txt
export MAILGUN_API_KEY="key-your-api-key"
export MAILGUN_DOMAIN="mg.yourdomain.com"
export MAILGUN_FROM="Epic Games Monitor <noreply@mg.yourdomain.com>"
export RECIPIENT_EMAIL="you@example.com"
python epic_games_monitor.py
```

## Troubleshooting

### Email Not Sending?
- Confirm `MAILGUN_API_KEY` is the **Private** API key, not the Public Validation key
- Make sure the sending domain is fully verified in Mailgun (DNS records propagated)
- If using the Mailgun sandbox domain, the recipient address must be added as an **Authorized Recipient** in the Mailgun dashboard
- Check the GitHub Actions log for the full error response from the API

### Script Not Running?
- Check the **Actions** tab for failed workflow runs
- Click on a failed run to see error details
- Verify all four secrets are set correctly

### Changes Not Saving?
- The script auto-commits `games_notified.json` after a successful send
- Check that GitHub Actions has write permission: **Settings** → **Actions** → **General** → **Workflow permissions** → set to **Read and write**

## Customization

### Change Run Time
Edit `.github/workflows/epic-games-monitor.yml`:
```yaml
- cron: '0 15 * * 4'  # Every Thursday at 3 PM UTC
```
Use [crontab.guru](https://crontab.guru) to calculate your preferred time.

## Notes

- Emails are sent in HTML format
- First run will notify about all currently free games
- Subsequent runs only email about newly added games
- GitHub provides 2,000+ free Actions minutes/month — more than enough for once-weekly runs
