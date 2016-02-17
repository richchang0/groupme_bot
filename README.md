This is a bot written in python, to interact with groupme.

Currently, it only writes the amount of messages sent in a groupme for a day.

To run, created a virtualenv

`virtualenv env`

source the environment and install the dependencies using pip

`source env/bin/activate && pip install -r requirements.txt`

add environment variables to your .bashrc

`export group_id=123`
`export bot_id=456`
`export access_token=abc123`

then run the app

`python clock.py`
