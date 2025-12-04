#!/usr/bin/env python3
"""
Billboard Chart Scraper
Scrapes Billboard Hot 100 and Hot 200 charts from Billboard.com
"""
import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime, timedelta
import time
import json

class BillboardScraper:
    def __init__(self):
        self.base_url = "https://www.billboard.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    def get_chart_date(self, date):
        """Format date for Billboard chart URL (YYYY-MM-DD)"""
        return date.strftime('%Y-%m-%d')

    def scrape_hot_100(self, date):
        """Scrape Billboard Hot 100 for a specific date"""
        chart_date = self.get_chart_date(date)
        url = f"{self.base_url}/charts/hot-100/{chart_date}"

        print(f"Scraping Hot 100 for {chart_date}...")

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find chart entries
            entries = []
            chart_items = soup.select('div.o-chart-results-list-row-container')

            for item in chart_items:
                try:
                    # Get rank (first span.c-label in the item)
                    rank_spans = item.select('span.c-label')
                    rank = rank_spans[0].text.strip() if len(rank_spans) > 0 else None

                    # Get song title
                    title_elem = item.select_one('h3.c-title')
                    title = title_elem.text.strip() if title_elem else None

                    # Get artist
                    artist_elem = item.select_one('span.c-label.a-no-trucate')
                    artist = artist_elem.text.strip() if artist_elem else None

                    # Get chart stats (last week, peak, weeks on chart)
                    stat_spans = item.select('span.c-label.u-font-family-secondary\\@mobile-max')
                    last_week = stat_spans[0].text.strip() if len(stat_spans) > 0 else None
                    peak = stat_spans[1].text.strip() if len(stat_spans) > 1 else None
                    weeks = stat_spans[2].text.strip() if len(stat_spans) > 2 else None

                    if rank and title and artist:
                        entries.append({
                            'date': chart_date,
                            'rank': rank,
                            'song': title,
                            'artist': artist,
                            'last_week': last_week if last_week and last_week != '-' else None,
                            'peak_position': peak if peak and peak != '-' else None,
                            'weeks_on_chart': weeks if weeks and weeks != '-' else None
                        })
                except Exception as e:
                    print(f"  Error parsing entry: {e}")
                    continue

            if not entries:
                print(f"  Warning: No entries found for {chart_date}")
            else:
                print(f"  Found {len(entries)} entries")

            return entries

        except requests.RequestException as e:
            print(f"  Error fetching Hot 100: {e}")
            return []

    def scrape_hot_200(self, date):
        """Scrape Billboard 200 (albums) for a specific date"""
        chart_date = self.get_chart_date(date)
        url = f"{self.base_url}/charts/billboard-200/{chart_date}"

        print(f"Scraping Billboard 200 for {chart_date}...")

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find chart entries
            entries = []
            chart_items = soup.select('div.o-chart-results-list-row-container')

            for item in chart_items:
                try:
                    # Get rank (first span.c-label in the item)
                    rank_spans = item.select('span.c-label')
                    rank = rank_spans[0].text.strip() if len(rank_spans) > 0 else None

                    # Get album title
                    title_elem = item.select_one('h3.c-title')
                    title = title_elem.text.strip() if title_elem else None

                    # Get artist
                    artist_elem = item.select_one('span.c-label.a-no-trucate')
                    artist = artist_elem.text.strip() if artist_elem else None

                    # Get chart stats (last week, peak, weeks on chart)
                    stat_spans = item.select('span.c-label.u-font-family-secondary\\@mobile-max')
                    last_week = stat_spans[0].text.strip() if len(stat_spans) > 0 else None
                    peak = stat_spans[1].text.strip() if len(stat_spans) > 1 else None
                    weeks = stat_spans[2].text.strip() if len(stat_spans) > 2 else None

                    if rank and title and artist:
                        entries.append({
                            'date': chart_date,
                            'rank': rank,
                            'album': title,
                            'artist': artist,
                            'last_week': last_week if last_week and last_week != '-' else None,
                            'peak_position': peak if peak and peak != '-' else None,
                            'weeks_on_chart': weeks if weeks and weeks != '-' else None
                        })
                except Exception as e:
                    print(f"  Error parsing entry: {e}")
                    continue

            if not entries:
                print(f"  Warning: No entries found for {chart_date}")
            else:
                print(f"  Found {len(entries)} entries")

            return entries

        except requests.RequestException as e:
            print(f"  Error fetching Billboard 200: {e}")
            return []

    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        if not data:
            print(f"No data to save for {filename}")
            return

        filepath = os.path.join(self.data_dir, filename)
        file_exists = os.path.isfile(filepath)

        # Read existing data to avoid duplicates
        existing_data = []
        if file_exists:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    existing_data = list(reader)
            except Exception as e:
                print(f"Error reading existing file: {e}")

        # Combine and deduplicate
        all_data = existing_data + data

        # Create a unique key for deduplication
        seen = set()
        unique_data = []
        for entry in all_data:
            # Create key from date and rank
            key = f"{entry.get('date')}_{entry.get('rank')}"
            if key not in seen:
                seen.add(key)
                unique_data.append(entry)

        # Sort by date and rank
        unique_data.sort(key=lambda x: (x.get('date', ''), int(x.get('rank', 0))))

        # Write to CSV
        if unique_data:
            fieldnames = unique_data[0].keys()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(unique_data)

            print(f"Saved {len(unique_data)} total entries to {filepath}")

    def get_last_thursday(self, from_date=None):
        """Get the most recent Thursday (Billboard release day)"""
        if from_date is None:
            from_date = datetime.now()

        # Billboard charts are dated on Saturdays but released on Tuesdays
        # We'll use Saturday dates for consistency
        days_since_saturday = (from_date.weekday() - 5) % 7
        last_saturday = from_date - timedelta(days=days_since_saturday)

        return last_saturday

    def generate_chart_dates(self, start_date, end_date):
        """Generate list of chart dates (Saturdays) between start and end dates"""
        dates = []
        current = self.get_last_thursday(start_date)
        end = self.get_last_thursday(end_date)

        while current <= end:
            dates.append(current)
            current += timedelta(days=7)

        return dates

    def scrape_range(self, start_date, end_date):
        """Scrape charts for a date range"""
        dates = self.generate_chart_dates(start_date, end_date)

        print(f"\n{'='*60}")
        print(f"Scraping Billboard Charts")
        print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print(f"Number of weeks: {len(dates)}")
        print(f"{'='*60}\n")

        hot_100_data = []
        hot_200_data = []

        for i, date in enumerate(dates, 1):
            print(f"\nWeek {i}/{len(dates)}: {date.strftime('%Y-%m-%d')}")
            print("-" * 40)

            # Scrape Hot 100
            hot_100_entries = self.scrape_hot_100(date)
            hot_100_data.extend(hot_100_entries)

            time.sleep(2)  # Be polite to the server

            # Scrape Billboard 200
            hot_200_entries = self.scrape_hot_200(date)
            hot_200_data.extend(hot_200_entries)

            time.sleep(2)  # Be polite to the server

        # Save data
        print(f"\n{'='*60}")
        print("Saving data...")
        print(f"{'='*60}\n")

        self.save_to_csv(hot_100_data, 'hot_100.csv')
        self.save_to_csv(hot_200_data, 'billboard_200.csv')

        print(f"\n{'='*60}")
        print("Scraping complete!")
        print(f"{'='*60}\n")

        return {
            'hot_100': len(hot_100_data),
            'billboard_200': len(hot_200_data)
        }

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Scrape Billboard charts')
    parser.add_argument('--weeks', type=int, default=1, help='Number of weeks to scrape (default: 1)')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')

    args = parser.parse_args()

    scraper = BillboardScraper()

    if args.start_date and args.end_date:
        start = datetime.strptime(args.start_date, '%Y-%m-%d')
        end = datetime.strptime(args.end_date, '%Y-%m-%d')
    else:
        # Default: scrape the last N weeks
        end = datetime.now()
        start = end - timedelta(weeks=args.weeks)

    scraper.scrape_range(start, end)

if __name__ == '__main__':
    main()
