#!/bin/bash

# Start the backend server
cd /home/ubuntu/MarketingPlatform/backend
export FLASK_APP=src.main
export FLASK_ENV=production
python -m flask run --host=0.0.0.0 --port=5000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start the frontend development server
cd /home/ubuntu/MarketingPlatform/frontend
pnpm run dev &
FRONTEND_PID=$!

echo "Marketing Platform started!"
echo "Backend running on http://localhost:5000"
echo "Frontend running on http://localhost:5173"
echo ""
echo "To stop the servers, run: kill $BACKEND_PID $FRONTEND_PID"

# Save the PIDs to a file for easy shutdown
echo "$BACKEND_PID $FRONTEND_PID" > /home/ubuntu/MarketingPlatform/server_pids.txt
