# Keyword Search Volume Counter

A modern web application that analyzes keyword search volumes across different countries (US, Canada, UK) for specific time periods using Google Trends data.

## Features

- 🔍 **Multi-keyword Analysis**: Analyze up to 5 keywords simultaneously
- 🌍 **Country Support**: United States, Canada, and United Kingdom
- 📅 **Custom Time Periods**: Specify start and end dates for analysis
- 📊 **Visual Charts**: Interactive trend charts showing search volume over time
- 📈 **Detailed Metrics**: Average, peak, and minimum search volumes
- 🎨 **Modern UI**: Beautiful, responsive design with gradient backgrounds

## Installation

1. **Clone or download this project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to `http://localhost:5000`

## Usage

1. **Enter Keywords**: Type your keywords separated by commas (e.g., "python programming, web development, data science")

2. **Select Country**: Choose from United States, Canada, or United Kingdom

3. **Set Time Period**: Pick your start and end dates for analysis

4. **Click Search**: The application will analyze the keywords and display results

## How It Works

- Uses the `pytrends` library to access Google Trends data
- Fetches relative search volume data for specified keywords and countries
- Calculates average, maximum, and minimum search volumes
- Generates interactive charts using Plotly
- Provides a clean, modern web interface

## Important Notes

- **Rate Limiting**: Google Trends has rate limits, so the app limits to 5 keywords per search
- **Relative Data**: Google Trends provides relative search volume (0-100 scale), not absolute numbers
- **Data Availability**: Some keywords may not have sufficient data for certain time periods
- **Free Service**: This tool uses free Google Trends data, which has some limitations compared to paid keyword research tools

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Source**: Google Trends via pytrends
- **Charts**: Plotly.js
- **Styling**: Custom CSS with modern design principles

## Troubleshooting

- If you encounter rate limiting errors, wait a few minutes before trying again
- Ensure your date range is valid (start date before end date)
- Some very specific or niche keywords may not return data
- Make sure all required fields are filled before submitting

## Future Enhancements

- Support for more countries
- Export functionality (CSV, PDF)
- Historical data comparison
- Keyword difficulty analysis
- Related keywords suggestions
