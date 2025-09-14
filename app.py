from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for n8n integration

# Country codes mapping
COUNTRIES = {
    'US': 'US',
    'CA': 'CA', 
    'UK': 'GB'
}

def get_search_volume_data(keywords, country, start_date, end_date):
    """
    Get search volume data for keywords in a specific country and time period
    """
    try:
        # Initialize pytrends
        pytrends = TrendReq(hl='en-US', tz=360)
        
        # Convert dates to proper format
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        # Build payload
        pytrends.build_payload(
            keywords, 
            cat=0, 
            timeframe=f'{start_date_str} {end_date_str}', 
            geo=country, 
            gprop=''
        )
        
        # Get interest over time data
        interest_over_time = pytrends.interest_over_time()
        
        if interest_over_time.empty:
            return None, "No data available for the specified criteria"
        
        # Calculate average search volume for each keyword
        results = {}
        for keyword in keywords:
            if keyword in interest_over_time.columns:
                avg_volume = interest_over_time[keyword].mean()
                results[keyword] = {
                    'average_volume': round(avg_volume, 2),
                    'max_volume': int(interest_over_time[keyword].max()),
                    'min_volume': int(interest_over_time[keyword].min()),
                    'trend_data': interest_over_time[keyword].to_dict()
                }
            else:
                results[keyword] = {
                    'average_volume': 0,
                    'max_volume': 0,
                    'min_volume': 0,
                    'trend_data': {}
                }
        
        return results, None
        
    except Exception as e:
        return None, str(e)

def create_trend_chart(keywords, country, start_date, end_date):
    """
    Create a trend chart for the keywords
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        pytrends.build_payload(
            keywords, 
            cat=0, 
            timeframe=f'{start_date_str} {end_date_str}', 
            geo=country, 
            gprop=''
        )
        
        interest_over_time = pytrends.interest_over_time()
        
        if interest_over_time.empty:
            return None
        
        # Create plotly figure
        fig = go.Figure()
        
        for keyword in keywords:
            if keyword in interest_over_time.columns:
                fig.add_trace(go.Scatter(
                    x=interest_over_time.index,
                    y=interest_over_time[keyword],
                    mode='lines+markers',
                    name=keyword,
                    line=dict(width=2)
                ))
        
        fig.update_layout(
            title=f'Search Volume Trends - {country}',
            xaxis_title='Date',
            yaxis_title='Relative Search Volume',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    except Exception as e:
        print(f"Error creating chart: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_keywords():
    try:
        data = request.get_json()
        keywords = [kw.strip() for kw in data['keywords'].split(',') if kw.strip()]
        country = data['country']
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        
        if not keywords:
            return jsonify({'error': 'Please provide at least one keyword'}), 400
        
        if country not in COUNTRIES:
            return jsonify({'error': 'Invalid country selected'}), 400
        
        if start_date >= end_date:
            return jsonify({'error': 'Start date must be before end date'}), 400
        
        # Limit to 5 keywords to avoid rate limiting
        if len(keywords) > 5:
            keywords = keywords[:5]
        
        # Get search volume data
        results, error = get_search_volume_data(keywords, COUNTRIES[country], start_date, end_date)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Create trend chart
        chart_json = create_trend_chart(keywords, COUNTRIES[country], start_date, end_date)
        
        return jsonify({
            'results': results,
            'chart': chart_json,
            'country': country,
            'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/search-volume', methods=['POST'])
def api_search_volume():
    """
    API endpoint specifically designed for n8n integration
    Expects JSON with: keywords (array), geo (string), startTime (ISO string), endTime (ISO string)
    """
    try:
        # Handle both single object and array of objects from n8n
        data = request.get_json()
        
        # If data is a list (from n8n), take the first item
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        # Extract keywords from the request
        keywords = data.get('keywords', [])
        if not keywords:
            return jsonify({
                'success': False,
                'error': 'No keywords provided',
                'data': None
            }), 400
        
        # Extract geo (country) - map to our country codes
        geo = data.get('geo', 'US').upper()
        if geo not in COUNTRIES:
            return jsonify({
                'success': False,
                'error': f'Invalid geo code: {geo}. Supported: US, CA, UK',
                'data': None
            }), 400
        
        # Extract and parse dates
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        
        if not start_time or not end_time:
            return jsonify({
                'success': False,
                'error': 'startTime and endTime are required',
                'data': None
            }), 400
        
        try:
            # Parse ISO datetime strings
            start_date = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use ISO 8601 format (e.g., 2025-08-01T00:00:00.000Z)',
                'data': None
            }), 400
        
        if start_date >= end_date:
            return jsonify({
                'success': False,
                'error': 'startTime must be before endTime',
                'data': None
            }), 400
        
        # Limit to 5 keywords to avoid rate limiting
        if len(keywords) > 5:
            keywords = keywords[:5]
        
        # Get search volume data
        results, error = get_search_volume_data(keywords, COUNTRIES[geo], start_date, end_date)
        
        if error:
            return jsonify({
                'success': False,
                'error': error,
                'data': None
            }), 400
        
        # Format response for n8n
        formatted_results = []
        for keyword, metrics in results.items():
            formatted_results.append({
                'keyword': keyword,
                'average_volume': metrics['average_volume'],
                'max_volume': metrics['max_volume'],
                'min_volume': metrics['min_volume'],
                'geo': geo,
                'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            })
        
        return jsonify({
            'success': True,
            'error': None,
            'data': {
                'keywords': formatted_results,
                'summary': {
                    'total_keywords': len(formatted_results),
                    'geo': geo,
                    'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                    'processed_at': datetime.now().isoformat()
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'data': None
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for n8n"""
    return jsonify({
        'status': 'healthy',
        'service': 'keyword-search-volume-api',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
