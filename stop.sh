kill $(ps aux | grep clock.py | grep -v grep | awk '{print $2}')
