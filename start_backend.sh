#!/bin/bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
nohup uvicorn main:app --host 0.0.0.0 --port 8005 > backend.log 2>&1 &
echo "Backend started with PID $!"
j