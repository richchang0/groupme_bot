PID=$(ps aux | grep clock.py | grep -v grep | awk '{print $2}')
if [ -z "$PID" ]; then
  . ~/envs/groupme/bin/activate
  rm /home/pi/groupme_bot/nohup.out
  nohup python /home/pi/groupme_bot/clock.py &
else
  echo "already running";
fi
