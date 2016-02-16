from groupme import send_daily_message_count
from apscheduler.schedulers.blocking import BlockingScheduler
import os

if __name__ == '__main__':
  sched = BlockingScheduler()
  sched.add_job(send_daily_message_count, 'cron', hour=23, minute=59, timezone='America/Chicago')
  print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
  try:
    sched.start()
  except (KeyboardInterrupt, SystemExit):
    pass
