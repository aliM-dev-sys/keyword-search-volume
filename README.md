# Keyword Search Volume API

A lightweight API service that provides keyword search volume data for n8n integration using Google Trends data.

## Features

- 🔍 **Multi-keyword Analysis**: Analyze up to 5 keywords simultaneously
- 🌍 **Country Support**: United States, Canada, and United Kingdom
- 📅 **Custom Time Periods**: Specify start and end dates for analysis
- 📈 **Detailed Metrics**: Average, peak, and minimum search volumes
- 🚀 **n8n Ready**: Optimized for n8n HTTP requests
- ⚡ **Lightweight**: Minimal dependencies and fast deployment

## API Endpoints

### Search Volume API
**POST** `/api/search-volume`

**Request Format:**
```json
{
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "geo": "US",
  "startTime": "2025-08-01T00:00:00.000Z",
  "endTime": "2025-08-31T00:00:00.000Z"
}
```

**Response Format:**
```json
{
  "success": true,
  "error": null,
  "data": {
    "keywords": [
      {
        "keyword": "keyword1",
        "average_volume": 45.2,
        "max_volume": 78,
        "min_volume": 23,
        "geo": "US",
        "period": "2025-08-01 to 2025-08-31"
      }
    ],
    "summary": {
      "total_keywords": 5,
      "geo": "US",
      "period": "2025-08-01 to 2025-08-31",
      "processed_at": "2024-01-15T10:30:00.000Z"
    }
  }
}
```

### Health Check
**GET** `/api/health`

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **For production with Gunicorn**:
   ```bash
   gunicorn --config gunicorn.conf.py app:app
   ```

## Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t keyword-search-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 keyword-search-api
   ```

## n8n Integration

See `n8n_integration_guide.md` for detailed integration instructions.

## Technical Details

- **Backend**: Flask (Python)
- **Data Source**: Google Trends via pytrends
- **WSGI Server**: Gunicorn
- **Container**: Docker optimized
- **Dependencies**: Minimal (Flask, pytrends, pandas, gunicorn)

## Important Notes

- **Rate Limiting**: Google Trends has rate limits, max 5 keywords per request
- **Relative Data**: Google Trends provides relative search volume (0-100 scale)
- **Data Availability**: Some keywords may not have sufficient data
- **Free Service**: Uses free Google Trends data with limitations
