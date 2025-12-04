# Billboard Chart Scraper

Automated web scraper that collects Billboard Hot 100 (songs) and Billboard 200 (albums) chart data directly from Billboard.com.

## Features

- Scrapes Billboard Hot 100 and Billboard 200 charts
- Stores data in CSV format
- Automatic weekly updates via GitHub Actions (every Wednesday at 00:00 UTC)
- Can backfill historical data
- Deduplicates entries automatically

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Scraper

#### Scrape Latest Week
```bash
python scraper.py
```

#### Scrape Multiple Weeks
```bash
python scraper.py --weeks 4
```

#### Scrape Specific Date Range
```bash
python scraper.py --start-date 2024-11-01 --end-date 2024-12-04
```

## Automated Updates

The scraper runs automatically every Wednesday at 00:00 UTC via GitHub Actions. This is one day after Billboard releases their charts (Tuesday).

### Manual Trigger

You can manually trigger the scraper from GitHub:
1. Go to the "Actions" tab in your repository
2. Select "Weekly Billboard Chart Scraper"
3. Click "Run workflow"

## Data Format

### Hot 100 CSV
- `date`: Chart date (YYYY-MM-DD)
- `rank`: Position on chart (1-100)
- `song`: Song title
- `artist`: Artist name
- `last_week`: Previous week's position
- `peak_position`: Highest position achieved
- `weeks_on_chart`: Total weeks on chart

### Billboard 200 CSV
- `date`: Chart date (YYYY-MM-DD)
- `rank`: Position on chart (1-200)
- `album`: Album title
- `artist`: Artist name

## Data Location

All scraped data is stored in the `data/` directory:
- `data/hot_100.csv` - Billboard Hot 100 songs
- `data/billboard_200.csv` - Billboard 200 albums

## How It Works

1. Billboard releases new charts every Tuesday
2. GitHub Actions triggers the scraper every Wednesday at 00:00 UTC
3. Scraper downloads the latest chart data from Billboard.com
4. Data is saved to CSV files in the `data/` directory
5. Changes are automatically committed and pushed to GitHub

## Notes

- The scraper includes delays between requests to be respectful to Billboard's servers
- Duplicate entries are automatically filtered out
- Chart dates are based on Saturday (Billboard's official chart date)
