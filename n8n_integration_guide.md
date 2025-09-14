# n8n Integration Guide

## API Endpoints

### 1. Main Search Volume API
**Endpoint:** `POST /api/search-volume`

**Purpose:** Get search volume data for keywords in specific countries and time periods

### 2. Health Check
**Endpoint:** `GET /api/health`

**Purpose:** Check if the API is running and healthy

## Request Format

The API accepts the exact format from your n8n HTTP node:

```json
[
  {
    "keywords": [
      "AI agent implementation small business US",
      "automated AI agents for small business operations",
      "small business AI assistant solutions",
      "cost-effective AI agents for SMBs",
      "AI agent benefits for small business growth"
    ],
    "geo": "US",
    "startTime": "2025-08-01T00:00:00.000Z",
    "endTime": "2025-08-31T00:00:00.000Z"
  }
]
```

### Required Fields:
- `keywords`: Array of strings (max 5 keywords)
- `geo`: Country code ("US", "CA", "UK")
- `startTime`: ISO 8601 datetime string
- `endTime`: ISO 8601 datetime string

### Optional Fields:
- Any additional fields will be ignored

## Response Format

### Success Response (200):
```json
{
  "success": true,
  "error": null,
  "data": {
    "keywords": [
      {
        "keyword": "AI agent implementation small business US",
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

### Error Response (400/500):
```json
{
  "success": false,
  "error": "Error message here",
  "data": null
}
```

## n8n Workflow Setup

### 1. HTTP Request Node Configuration

**Method:** POST
**URL:** `https://your-server.com/api/search-volume`
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "keywords": ["{{ $json.keywords }}"],
  "geo": "{{ $json.geo }}",
  "startTime": "{{ $json.startTime }}",
  "endTime": "{{ $json.endTime }}"
}
```

### 2. Parallel Processing Setup

For your 3 parallel requests with 5 keywords each:

1. **Split your 15 keywords into 3 groups of 5**
2. **Create 3 HTTP Request nodes in parallel**
3. **Each node processes 5 keywords**
4. **Merge results using a Merge node**

### 3. Example n8n Workflow

```
[Webhook] → [Split Keywords] → [HTTP Request 1] ┐
                ↓              [HTTP Request 2] ┼→ [Merge] → [Response]
                ↓              [HTTP Request 3] ┘
```

## Deployment Considerations

### 1. Server Requirements
- Python 3.8+
- At least 512MB RAM
- Internet connection for Google Trends API

### 2. Environment Variables
Create a `.env` file:
```
FLASK_ENV=production
FLASK_DEBUG=False
```

### 3. Production Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with uWSGI
pip install uwsgi
uwsgi --http :5000 --module app:app --processes 4 --threads 2
```

### 4. Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Rate Limiting & Best Practices

### 1. Rate Limits
- Google Trends has rate limits
- Max 5 keywords per request
- Wait 1-2 seconds between requests
- Consider implementing request queuing

### 2. Error Handling
- Always check `success` field in response
- Handle rate limiting errors gracefully
- Implement retry logic with exponential backoff

### 3. Caching
- Consider caching results for repeated queries
- Implement Redis or similar for production

## Testing

Run the test script to verify your setup:

```bash
python test_n8n_api.py
```

This will test:
1. Health check endpoint
2. Full n8n request format
3. Simplified request format

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure Flask-CORS is installed and configured
2. **Rate Limiting**: Implement delays between requests
3. **Date Format**: Ensure dates are in ISO 8601 format
4. **Keyword Limits**: Max 5 keywords per request

### Debug Mode:
Set `FLASK_DEBUG=True` for detailed error messages in development.

## Support

For issues or questions:
1. Check the health endpoint first
2. Verify request format matches examples
3. Check server logs for detailed error messages
4. Test with the provided test script
