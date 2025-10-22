# Billboard Chart Analyzer

A Python tool to analyze and visualize Billboard chart performance for any artist across multiple chart types (Hot 100, Radio Songs, and Streaming Songs).

## Prerequisites

- macOS
- Python 3 (usually pre-installed on Mac)
- Terminal access

## Installation

### 1. Install Required Python Libraries

Open Terminal and run:
```bash
pip3 install pandas openpyxl
```

If that doesn't work, try:
```bash
python3 -m pip install pandas openpyxl
```

### 2. Download the Dataset

1. Go to the Kaggle dataset page: https://www.kaggle.com/datasets/ludmin/billboard
2. Click the **Download** button (you may need to create a free Kaggle account)
3. Extract the downloaded ZIP file
4. You'll find several CSV files including:
   - `hot100.csv` (or `billboard200.csv`)
   - `radio.csv`
   - `streaming_songs.csv`

### 3. Move CSV Files to Desktop

Move the CSV files you want to analyze to your Desktop:
```bash
mv ~/Downloads/hot100.csv ~/Desktop/
mv ~/Downloads/radio.csv ~/Desktop/
mv ~/Downloads/streaming_songs.csv ~/Desktop/
```

Or simply drag and drop them from your Downloads folder to your Desktop.

## Usage

### Billboard Hot 100 / Billboard 200 Analysis

1. Create a new file called `billboard_analysis.py` on your Desktop
2. Copy this code into it:
```python
import os
import pandas as pd

# === PARAMETERS TO EDIT ===
artist_name = 'Taylor Swift'  # ← enter the artist name here

# Direct path with your username
file_path = '/Users/prangonbarua/Desktop/hot100.csv'  # or billboard200.csv
# ===========================

# Load the data
data = pd.read_csv(file_path, low_memory=False)

# Check if all required columns are present
required_cols = {'Date', 'Song', 'Artist', 'Rank'}
if required_cols.issubset(data.columns):
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date'])

    # Clean text fields
    data['Song'] = data['Song'].str.strip().str.lower()
    data['Artist'] = data['Artist'].str.strip().str.lower()

    # Filter by artist
    filtered_data = data[data['Artist'].str.contains(artist_name.lower(), na=False)]

    if not filtered_data.empty:
        # Create a 'Song (Artist)' column
        filtered_data = filtered_data.copy()
        filtered_data['Song_Artist'] = (
            filtered_data['Song'].str.title() + " (" + filtered_data['Artist'].str.title() + ")"
        )

        # Pivot table using actual dates from the data
        pivot_table = filtered_data.pivot_table(
            index='Date', 
            columns='Song_Artist', 
            values='Rank',
            aggfunc='first'
        )

        # Fill in missing weeks
        all_dates = pd.Series(data['Date'].unique())
        all_dates = all_dates[all_dates >= filtered_data['Date'].min()]
        pivot_table = pivot_table.reindex(pd.to_datetime(sorted(all_dates)))

        # Sort columns by first appearance
        first_appearance = filtered_data.groupby('Song_Artist')['Date'].min()
        sorted_columns = first_appearance.sort_values().index
        pivot_table = pivot_table[sorted_columns]

        # Format index as text
        pivot_table.index = pivot_table.index.strftime('%Y-%m-%d')

        # Safe filename for output
        safe_name = artist_name.title().replace(" ", "_")
        
        # Output file path to Desktop
        output_file = f'/Users/prangonbarua/Desktop/{safe_name}_Chart_History.xlsx'

        # Save to Excel
        pivot_table.to_excel(output_file)

        print(f"✅ Done! Data for '{artist_name.title()}' saved to: {output_file}")
    else:
        print(f"⚠️ No results found for artist: {artist_name}")
else:
    print("❌ Missing required columns. Found columns:", data.columns.tolist())
```

3. Edit the `artist_name` variable (line 6) to analyze your desired artist
4. Run the script:
```bash
cd ~/Desktop
python3 billboard_analysis.py
```

### Radio Songs Analysis

1. Create `radio_analysis.py` on your Desktop
2. Copy this code:
```python
import os
import pandas as pd

# === PARAMETERS TO EDIT ===
artist_name = 'Taylor Swift'  # ← enter the artist name here

# Direct path with your username
file_path = '/Users/prangonbarua/Desktop/radio.csv'
# ===========================

# Load the data
data = pd.read_csv(file_path, low_memory=False)

# Check if all required columns are present
required_cols = {'Date', 'Song', 'Artist', 'Rank'}
if required_cols.issubset(data.columns):
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date'])

    # Clean text fields
    data['Song'] = data['Song'].str.strip().str.lower()
    data['Artist'] = data['Artist'].str.strip().str.lower()

    # Filter by artist
    filtered_data = data[data['Artist'].str.contains(artist_name.lower(), na=False)]

    if not filtered_data.empty:
        # Create a 'Song (Artist)' column
        filtered_data = filtered_data.copy()
        filtered_data['Song_Artist'] = (
            filtered_data['Song'].str.title() + " (" + filtered_data['Artist'].str.title() + ")"
        )

        # Pivot table using actual dates from the data
        pivot_table = filtered_data.pivot_table(
            index='Date', 
            columns='Song_Artist', 
            values='Rank',
            aggfunc='first'
        )

        # Fill in missing weeks
        all_dates = pd.Series(data['Date'].unique())
        all_dates = all_dates[all_dates >= filtered_data['Date'].min()]
        pivot_table = pivot_table.reindex(pd.to_datetime(sorted(all_dates)))

        # Sort columns by first appearance
        first_appearance = filtered_data.groupby('Song_Artist')['Date'].min()
        sorted_columns = first_appearance.sort_values().index
        pivot_table = pivot_table[sorted_columns]

        # Format index as text
        pivot_table.index = pivot_table.index.strftime('%Y-%m-%d')

        # Safe filename for output
        safe_name = artist_name.title().replace(" ", "_")
        
        # Output file path to Desktop
        output_file = f'/Users/prangonbarua/Desktop/{safe_name}_Radio_Chart_History.xlsx'

        # Save to Excel
        pivot_table.to_excel(output_file)

        print(f"✅ Done! Radio chart data for '{artist_name.title()}' saved to: {output_file}")
    else:
        print(f"⚠️ No results found for artist: {artist_name}")
else:
    print("❌ Missing required columns. Found columns:", data.columns.tolist())
```

3. Edit the artist name and run:
```bash
python3 radio_analysis.py
```

### Streaming Songs Analysis

1. Create `streaming_analysis.py` on your Desktop
2. Copy this code:
```python
import os
import pandas as pd

# === PARAMETERS TO EDIT ===
artist_name = 'Taylor Swift'  # ← enter the artist name here

# Direct path with your username
file_path = '/Users/prangonbarua/Desktop/streaming_songs.csv'
# ===========================

# Load the data
data = pd.read_csv(file_path, low_memory=False)

# Check if all required columns are present
required_cols = {'Date', 'Song', 'Artist', 'Rank'}
if required_cols.issubset(data.columns):
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date'])

    # Clean text fields
    data['Song'] = data['Song'].str.strip().str.lower()
    data['Artist'] = data['Artist'].str.strip().str.lower()

    # Filter by artist
    filtered_data = data[data['Artist'].str.contains(artist_name.lower(), na=False)]

    if not filtered_data.empty:
        # Create a 'Song (Artist)' column
        filtered_data = filtered_data.copy()
        filtered_data['Song_Artist'] = (
            filtered_data['Song'].str.title() + " (" + filtered_data['Artist'].str.title() + ")"
        )

        # Pivot table using actual dates from the data
        pivot_table = filtered_data.pivot_table(
            index='Date', 
            columns='Song_Artist', 
            values='Rank',
            aggfunc='first'
        )

        # Fill in missing weeks
        all_dates = pd.Series(data['Date'].unique())
        all_dates = all_dates[all_dates >= filtered_data['Date'].min()]
        pivot_table = pivot_table.reindex(pd.to_datetime(sorted(all_dates)))

        # Sort columns by first appearance
        first_appearance = filtered_data.groupby('Song_Artist')['Date'].min()
        sorted_columns = first_appearance.sort_values().index
        pivot_table = pivot_table[sorted_columns]

        # Format index as text
        pivot_table.index = pivot_table.index.strftime('%Y-%m-%d')

        # Safe filename for output
        safe_name = artist_name.title().replace(" ", "_")
        
        # Output file path to Desktop
        output_file = f'/Users/prangonbarua/Desktop/{safe_name}_Streaming_Chart_History.xlsx'

        # Save to Excel
        pivot_table.to_excel(output_file)

        print(f"✅ Done! Streaming chart data for '{artist_name.title()}' saved to: {output_file}")
    else:
        print(f"⚠️ No results found for artist: {artist_name}")
else:
    print("❌ Missing required columns. Found columns:", data.columns.tolist())
```

3. Edit the artist name and run:
```bash
python3 streaming_analysis.py
```

## Output

Each script will generate an Excel file (`.xlsx`) on your Desktop with the format:
- `Artist_Name_Chart_History.xlsx` (for Billboard)
- `Artist_Name_Radio_Chart_History.xlsx` (for Radio)
- `Artist_Name_Streaming_Chart_History.xlsx` (for Streaming)

The Excel file contains:
- Rows: Dates (weekly chart dates)
- Columns: Songs by that artist
- Values: Chart position (rank) for each song on each date

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
Run: `pip3 install pandas openpyxl`

### "FileNotFoundError"
Make sure the CSV files are on your Desktop and named correctly:
- `hot100.csv` (or `billboard200.csv`)
- `radio.csv`
- `streaming_songs.csv`

### "No results found for artist"
- Check the spelling of the artist name
- Try using partial names (e.g., "Taylor" instead of "Taylor Swift")
- The artist might not be in that particular chart dataset

### Wrong username in file path
If your username is NOT `prangonbarua`, update the file paths in the code:
```python
file_path = '/Users/YOUR_USERNAME/Desktop/filename.csv'
output_file = f'/Users/YOUR_USERNAME/Desktop/{safe_name}_Chart_History.xlsx'
```

Or use the universal path:
```python
file_path = os.path.expanduser('~/Desktop/filename.csv')
output_file = os.path.expanduser(f'~/Desktop/{safe_name}_Chart_History.xlsx')
```

## Data Source

Dataset provided by Kaggle user Ludmin:
https://www.kaggle.com/datasets/ludmin/billboard

## License

This tool is for educational and personal use. The Billboard chart data is owned by Billboard and Luminate (formerly MRC Data/Nielsen Music).
