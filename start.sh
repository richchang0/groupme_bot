PID=$(ps aux | grep clock.py | grep -v grep | awk '{print $2}')
if [ -z "$PID" ]; then
  . env/bin/activate
  nohup /home/pi/groupme_bot/clock.py &  
else
  echo "already running";
fi
