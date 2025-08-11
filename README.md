# Autonomous Email Inbox Dashboard

A clean, simple Flask application that displays email processing statistics from LangSmith.

## 🚀 Quick Deploy to Vercel

1. **Fork/Clone this repository**
2. **Deploy to Vercel** using the "Import Git Repository" option
3. **Add Environment Variables** in Vercel dashboard

## 🔧 Environment Variables

Add these in your Vercel project settings:

```
LANGSMITH_API_KEY=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
GRAPH_ID=email_assistant_hitl_memory_gmail
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

## 📁 Project Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel configuration
├── templates/         # HTML templates
│   └── dashboard.html # Dashboard template
└── README.md          # This file
```

## 🎯 Features

- Real-time email statistics from LangSmith
- Clean, responsive dashboard
- Auto-refresh every 30 seconds
- Error handling and fallbacks

## 🔍 How It Works

1. Connects to LangSmith API using your API key
2. Fetches email processing runs from your project
3. Displays statistics and recent email threads
4. Updates automatically

## ✅ Requirements

- Python 3.9+
- Flask 2.3.3
- requests 2.31.0
- python-dotenv 1.0.0

## 🚨 Troubleshooting

If you see "pip command not found" errors:
- This project uses standard `requirements.txt` (not uv)
- Vercel will automatically install dependencies
- Make sure all environment variables are set correctly
