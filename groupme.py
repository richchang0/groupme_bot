import os
import calendar
import datetime
from dateutil import tz
import requests
import time
requests.packages.urllib3.disable_warnings()

bot_id  = os.environ["bot_id"]
access_token = os.environ["access_token"]
group_id = os.environ["group_id"]

def get_messages(limit=100, before_id='', after_id=''):
  data = {
           "access_token": access_token,
           "limit": limit,
           "before_id": before_id,
           "after_id": after_id
         }
  response = requests.get('https://api.groupme.com/v3/groups/%s/messages' % group_id, params=data)
  return response.json()

#looks backward
def find_messageid_before_timestamp(timestamp, start_id=None):
  batch_found = False
  batch = get_messages(limit=100)["response"]["messages"]
  while not batch_found:
    if batch[-1]['created_at'] < timestamp:
      batch_found = True
    else:
      last_id = batch[-1]['id']
      batch = get_messages(limit=100, before_id=last_id)["response"]["messages"]

  for i, message in enumerate(batch):
    if message['created_at'] < timestamp:
      return batch[i]['id']

def find_messages_after_timestamp(start_timestamp):
  message_id_just_before = find_messageid_before_timestamp(start_timestamp)
  messages = []
  done = False
  while not done:
    response = get_messages(after_id=message_id_just_before)['response']['messages']
    messages.extend(response)
    if len(response) < 100:
      done = True
    else:
      message_id_just_before = response[-1]['id']
  return messages

def prev_midnight():
  ONE_DAY = 86400
  SIX_HOURS = 21600
  now = calendar.timegm(time.gmtime())
  return now - (calendar.timegm(time.gmtime()) % ONE_DAY) + SIX_HOURS

def find_messages_since_midnight():
  return find_messages_after_timestamp(prev_midnight())

def send_message_to_group(bot_id, msg):
  data = {
           "bot_id": bot_id,
           "text": msg
         }
  requests.post('https://api.groupme.com/v3/bots/post', data=data)

def epoch_to_local(timestamp, timezone='America/Chicago'):
  utc = datetime.datetime.fromtimestamp(int(timestamp))
  from_zone = tz.tzutc()
  to_zone = tz.gettz(timezone)
  utc = utc.replace(tzinfo=from_zone)
  local = utc.astimezone(to_zone)
  return local

def send_daily_message_count():
  count = len(find_messages_since_midnight())
  date_str = epoch_to_local(prev_midnight()).strftime("%b %d %I:%M%p %Z")
  msg = "Since %s, there were %d messages" % (date_str, count)
  send_message_to_group(bot_id, msg)

def tell_frank_to_go_home():
  send_message_to_group(bot_id, "go home frank")

def startup_message():
  send_message_to_group(bot_id, "i'm back bois")

if __name__ == "__main__":
  print "manual test run"
  bot_id  = os.environ["testbot_id"]
  send_daily_message_count()
