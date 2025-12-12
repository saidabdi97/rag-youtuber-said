#!/bin/bash

echo "🚀 Starting FastAPI backend..."
uvicorn src.api.main:app --reload &
BACKEND_PID=$!

sleep 2

echo "🎨 Starting Streamlit frontend..."
streamlit run src/frontend/app.py &
FRONTEND_PID=$!

echo ""
echo "🔥 Both servers are running!"
echo "➡ Backend:  http://127.0.0.1:8000"
echo "➡ Frontend: http://localhost:8501"
echo ""
echo "Press CTRL + C to stop both."

wait $BACKEND_PID $FRONTEND_PID
