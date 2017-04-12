from groupme import send_daily_message_count, tell_frank_to_go_home, startup_message
from apscheduler.schedulers.blocking import BlockingScheduler
import os

if __name__ == '__main__':
  startup_message()
  sched = BlockingScheduler()
  sched.add_job(send_daily_message_count, 'cron', hour=23, minute=59, timezone='America/Chicago')
  sched.add_job(tell_frank_to_go_home, 'cron', hour=6, day_of_week='mon-fri', timezone='America/Los_Angeles')
  print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
  try:
    sched.start()
  except (KeyboardInterrupt, SystemExit):
    pass
