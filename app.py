from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# LangSmith Configuration
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
GRAPH_ID = os.getenv("GRAPH_ID")

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        # Get data from LangSmith
        data = get_langsmith_data()
        return render_template('dashboard.html', data=data)
    except Exception as e:
        error_data = {
            "statistics": {"total_emails": 0, "processed": 0, "hitl": 0, "ignored": 0},
            "emails": [],
            "error": str(e)
        }
        return render_template('dashboard.html', data=error_data)

@app.route('/api/refresh')
def api_refresh():
    """API endpoint for dashboard refresh"""
    try:
        data = get_langsmith_data()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_langsmith_data():
    """Fetch data from LangSmith API"""
    if not LANGSMITH_API_KEY:
        raise Exception("LANGSMITH_API_KEY not configured")
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': LANGSMITH_API_KEY
    }
    
    # Search for runs in the project
    search_url = f"{LANGSMITH_ENDPOINT}/runs/search"
    payload = {
        "project": GRAPH_ID,
        "limit": 100
    }
    
    response = requests.post(search_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        runs = response.json().get('runs', [])
        
        # Process the data
        total_emails = len(runs)
        processed = len([r for r in runs if r.get('status') == 'completed'])
        hitl = len([r for r in runs if r.get('status') == 'interrupted'])
        ignored = len([r for r in runs if r.get('status') == 'failed'])
        
        # Format email threads
        emails = []
        for run in runs[:20]:  # Show last 20
            emails.append({
                'id': run.get('id', ''),
                'subject': run.get('name', 'Email Processing'),
                'status': map_status(run.get('status', 'unknown')),
                'timestamp': run.get('start_time', ''),
                'thread_id': run.get('trace_id', '')
            })
        
        return {
            "statistics": {
                "total_emails": total_emails,
                "processed": processed,
                "hitl": hitl,
                "ignored": ignored,
                "waiting_action": 0,
                "scheduled_meetings": 0,
                "notifications": 0
            },
            "emails": emails,
            "last_updated": datetime.now().isoformat()
        }
    else:
        raise Exception(f"LangSmith API error: {response.status_code}")

def map_status(status):
    """Map LangSmith status to dashboard status"""
    status_map = {
        'completed': 'processed',
        'interrupted': 'hitl',
        'failed': 'ignored',
        'running': 'waiting_action',
        'pending': 'waiting_action'
    }
    return status_map.get(status, 'unknown')

if __name__ == '__main__':
    app.run(debug=True)
