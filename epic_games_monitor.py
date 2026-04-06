#!/usr/bin/env python3
"""
Epic Games Free Games Monitor
Monitors Epic Games free weekly games and sends email notifications
"""

import os
import json
import requests
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

# Configuration
GAMES_DATA_FILE = "games_notified.json"
EPIC_GAMES_API = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"


def fetch_free_games() -> List[Dict]:
    """Fetch current free games from Epic Games API"""
    try:
        response = requests.get(EPIC_GAMES_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        free_games = []
        
        if "data" in data and "Catalog" in data["data"]:
            promotions = data["data"]["Catalog"]["searchStore"]["elements"]
            
            for game in promotions:
                if not game.get("price") or not game["price"].get("totalPrice"):
                    continue
                
                # Check if game is free
                current_price = game["price"]["totalPrice"].get("discountPrice", 0)
                original_price = game["price"]["totalPrice"].get("originalPrice", 0)
                
                if current_price == 0 and original_price > 0:
                    # Get promotion end date
                    promotion_end = "Unknown"
                    if "promotions" in game and game["promotions"]:
                        for promo in game["promotions"]["promotionalOffers"]:
                            if promo["promotionalOffers"]:
                                promo_date = promo["promotionalOffers"][0]["endDate"]
                                promotion_end = promo_date[:10]  # Just the date
                    
                    free_games.append({
                        "title": game.get("title", "Unknown"),
                        "description": game.get("description", "No description"),
                        "image": game.get("keyImages", [{}])[0].get("url", ""),
                        "promotion_end": promotion_end,
                        "url": f"https://www.epicgames.com/store/en-US/p/{game.get('catalogNs', {}).get('mappings', [{}])[0].get('pageSlug', '')}",
                    })
        
        return free_games
    
    except Exception as e:
        print(f"Error fetching games: {e}")
        return []


def load_notified_games() -> set:
    """Load previously notified game IDs"""
    if os.path.exists(GAMES_DATA_FILE):
        with open(GAMES_DATA_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("notified_games", []))
    return set()


def save_notified_games(game_ids: set):
    """Save notified game IDs to file"""
    with open(GAMES_DATA_FILE, "w") as f:
        json.dump({"notified_games": list(game_ids)}, f)


def get_new_games(all_games: List[Dict], notified: set) -> List[Dict]:
    """Return only new games not previously notified"""
    new_games = []
    for game in all_games:
        game_id = game["title"].lower().replace(" ", "_")
        if game_id not in notified:
            new_games.append(game)
    return new_games


def send_email(recipient_email: str, games: List[Dict]):
    """Send email with game information"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("GMAIL_ADDRESS")
    sender_password = os.getenv("GMAIL_PASSWORD")  # App password, not actual password
    
    if not sender_email or not sender_password:
        print("Error: GMAIL_ADDRESS and GMAIL_PASSWORD environment variables not set")
        return False
    
    try:
        # Create email
        msg = MIMEMultipart("html")
        msg["Subject"] = f"🎮 Epic Games Free Games - {datetime.now().strftime('%B %d, %Y')}"
        msg["From"] = sender_email
        msg["To"] = recipient_email
        
        # Build HTML content
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #1f2937; border-bottom: 3px solid #2563eb; padding-bottom: 10px;">
                        🎮 Epic Games Free Games This Week
                    </h2>
                    <p style="color: #666;">Hello! Here are the new free games available on Epic Games:</p>
        """
        
        for game in games:
            html_content += f"""
                    <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; margin: 15px 0; background: #f9fafb;">
                        <h3 style="margin-top: 0; color: #1f2937;">{game['title']}</h3>
                        <p style="color: #666;">{game['description'][:200]}...</p>
                        <p style="font-size: 0.9em; color: #999;">
                            <strong>Free Until:</strong> {game['promotion_end']}
                        </p>
                        <a href="{game['url']}" style="display: inline-block; background: #2563eb; color: white; padding: 10px 20px; border-radius: 4px; text-decoration: none;">
                            Claim Game on Epic Games
                        </a>
                    </div>
            """
        
        html_content += """
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                    <p style="font-size: 0.9em; color: #999;">
                        This is an automated email from your Epic Games Free Games Monitor.
                    </p>
                </div>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(html_content, "html"))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✓ Email sent successfully to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        return False


def main():
    """Main function"""
    recipient_email = os.getenv("RECIPIENT_EMAIL", os.getenv("GMAIL_ADDRESS"))
    
    if not recipient_email:
        print("Error: RECIPIENT_EMAIL environment variable not set")
        return
    
    print("Fetching Epic Games free games...")
    all_games = fetch_free_games()
    
    if not all_games:
        print("No free games found or API error occurred")
        return
    
    print(f"Found {len(all_games)} free games")
    
    # Get new games
    notified = load_notified_games()
    new_games = get_new_games(all_games, notified)
    
    if not new_games:
        print("No new games to notify about")
        return
    
    print(f"Found {len(new_games)} new game(s)")
    
    # Send email
    if send_email(recipient_email, new_games):
        # Save notified games
        for game in new_games:
            notified.add(game["title"].lower().replace(" ", "_"))
        save_notified_games(notified)
        print("✓ New games recorded")
    else:
        print("✗ Failed to send email, games not recorded")


if __name__ == "__main__":
    main()
