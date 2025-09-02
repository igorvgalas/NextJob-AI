#!/bin/bash

LOG="/Users/cheef/Documents/nextjob-ai/services/gmail_reader/cron.log"

{
  echo "=== Cron START $(date) ==="
  whoami
  pwd
  echo "Python path: $(which python)"
  cd /Users/cheef/Documents/nextjob-ai/services/gmail_reader || {
    echo "Cannot cd to target directory"
    exit 1
  }

  echo "In directory: $(pwd)"
  echo "Activating venv..."
  source venv/bin/activate || echo "⚠️ venv activation failed"

  echo "Running main.py..."
  /Users/cheef/Documents/nextjob-ai/services/gmail_reader/venv/bin/python main.py

  echo "=== Cron END ==="
} >> "$LOG" 2>&1