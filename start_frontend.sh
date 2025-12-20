#!/bin/bash
cd mobile/build/web
nohup python3 -m http.server 8080 > web_server.log 2>&1 &
echo "Frontend started with PID $!"
