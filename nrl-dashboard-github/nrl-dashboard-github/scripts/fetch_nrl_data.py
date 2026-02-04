#!/usr/bin/env python3
"""
Fetch latest NRL data from multiple sources
Run daily via GitHub Actions to keep dashboard updated
"""

import requests
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Configuration
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_nrl_ladder():
    """Fetch current NRL ladder from NRL.com or fallback sources"""
    print("Fetching NRL ladder...")
    
    # Try NRL.com API (unofficial)
    try:
        # This endpoint may change - check network tab on nrl.com/ladder
        url = "https://www.nrl.com/api/v1/competitions/premiership/standings"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Fetched ladder from NRL.com")
            return data
    except Exception as e:
        print(f"NRL.com API failed: {e}")
    
    # Fallback: scrape from a public source
    try:
        url = "https://www.liveladders.com/nrl/"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Parse ladder table - structure varies by site
            print("✓ Fetched ladder from liveladders.com")
            return parse_ladder_html(soup)
    except Exception as e:
        print(f"Fallback ladder fetch failed: {e}")
    
    return None

def fetch_fixtures():
    """Fetch upcoming NRL fixtures"""
    print("Fetching NRL fixtures...")
    
    try:
        # Try NRL.com draw page
        url = "https://www.nrl.com/draw/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Parse fixtures from page
            soup = BeautifulSoup(response.text, 'html.parser')
            print("✓ Fetched fixtures")
            return parse_fixtures_html(soup)
    except Exception as e:
        print(f"Fixtures fetch failed: {e}")
    
    return None

def fetch_live_scores():
    """Fetch live scores during game time"""
    print("Checking for live games...")
    
    try:
        # Multiple potential sources for live scores
        sources = [
            "https://www.nrl.com/draw/?competition=111&round=1&season=2026",
            "https://www.flashscore.com/rugby-league/australia/nrl/",
        ]
        
        for url in sources:
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                if response.status_code == 200:
                    # Parse live scores
                    return parse_live_scores(response.text)
            except:
                continue
                
    except Exception as e:
        print(f"Live scores fetch failed: {e}")
    
    return None

def fetch_results():
    """Fetch completed match results"""
    print("Fetching recent results...")
    
    try:
        url = "https://www.rugbyleagueproject.org/seasons/nrl-2026/results.html"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print("✓ Fetched results from Rugby League Project")
            return parse_results_html(soup)
    except Exception as e:
        print(f"Results fetch failed: {e}")
    
    return None

def parse_ladder_html(soup):
    """Parse ladder HTML into structured data"""
    ladder = []
    # Implementation depends on source HTML structure
    # This is a template - adjust selectors based on actual source
    table = soup.find('table', class_='ladder') or soup.find('table')
    if table:
        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 8:
                ladder.append({
                    'position': len(ladder) + 1,
                    'team': cols[1].get_text(strip=True),
                    'played': int(cols[2].get_text(strip=True) or 0),
                    'wins': int(cols[3].get_text(strip=True) or 0),
                    'draws': int(cols[4].get_text(strip=True) or 0),
                    'losses': int(cols[5].get_text(strip=True) or 0),
                    'points_for': int(cols[6].get_text(strip=True) or 0),
                    'points_against': int(cols[7].get_text(strip=True) or 0),
                    'points': int(cols[-1].get_text(strip=True) or 0),
                })
    return ladder

def parse_fixtures_html(soup):
    """Parse fixtures HTML into structured data"""
    fixtures = []
    # Implementation depends on source
    return fixtures

def parse_live_scores(html):
    """Parse live scores from HTML"""
    scores = []
    # Implementation depends on source
    return scores

def parse_results_html(soup):
    """Parse results HTML into structured data"""
    results = []
    # Implementation depends on source
    return results

def save_data(data, filename):
    """Save data to JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Saved {filepath}")

def main():
    print(f"\n{'='*50}")
    print(f"NRL Data Fetch - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # Fetch all data
    ladder = fetch_nrl_ladder()
    fixtures = fetch_fixtures()
    results = fetch_results()
    live_scores = fetch_live_scores()
    
    # Save data
    timestamp = datetime.now().isoformat()
    
    all_data = {
        'last_updated': timestamp,
        'ladder': ladder,
        'fixtures': fixtures,
        'results': results,
        'live_scores': live_scores
    }
    
    save_data(all_data, 'nrl_live_data.json')
    
    # Also save individual files
    if ladder:
        save_data({'updated': timestamp, 'data': ladder}, 'ladder.json')
    if fixtures:
        save_data({'updated': timestamp, 'data': fixtures}, 'fixtures.json')
    if results:
        save_data({'updated': timestamp, 'data': results}, 'results.json')
    
    print(f"\n✓ Data fetch complete!")

if __name__ == "__main__":
    main()
