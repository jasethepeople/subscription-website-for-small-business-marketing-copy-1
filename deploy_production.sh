#!/bin/bash

# Stop any running servers
if [ -f "/home/ubuntu/MarketingPlatform/server_pids.txt" ]; then
  PIDS=$(cat /home/ubuntu/MarketingPlatform/server_pids.txt)
  kill $PIDS 2>/dev/null
  rm /home/ubuntu/MarketingPlatform/server_pids.txt
  echo "Stopped previous servers"
  sleep 2
fi

# Create production build for frontend
cd /home/ubuntu/MarketingPlatform/frontend
echo "Building frontend production assets..."
npm run build

# Start the backend with gunicorn
cd /home/ubuntu/MarketingPlatform/backend
echo "Starting backend with gunicorn..."
gunicorn --bind 0.0.0.0:5000 "src.main:app" --daemon

echo "Marketing Platform deployed in production mode!"
echo "Backend running on port 5000"
echo "Frontend static files ready for serving"
