import os
import calendar
import datetime
import requests
import time
requests.packages.urllib3.disable_warnings()

bot_id  = os.environ["bot_id"]
access_token = os.environ["groupme_token"]
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

def find_days_of_messages():
  current_time = calendar.timegm(time.gmtime())
  twenty_four_hours = 24*60*60
  return find_messages_after_timestamp(current_time - twenty_four_hours)

def send_message_to_group(bot_id, msg):
  data = {
           "bot_id": bot_id,
           "text": msg
         }
  requests.post('https://api.groupme.com/v3/bots/post', data=data)

def send_daily_message_count():
  count = len(find_days_of_messages())
  msg = "In the past 24 hours, there were %d messages" % count
  send_message_to_group(bot_id, msg)
