import json
import datetime
import time
import sys
from urllib import request, parse

global MEETUP_USERS, GROUP_NAME, BOT_TOKEN, CHAT_ID
EVENT_FILTER = ''
USERS_FILENAME = 'users.txt'


class MeetupUser:
    def __init__(self, api_key, name):
        self.api_key = api_key
        self.name = name


def init_meetup_users(list):
    with open(USERS_FILENAME, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue    # comment
            else:
                try:
                    name, api = line.split(' ')
                    api = api[:-1] # Removing \n
                    user = MeetupUser(api, name)
                    list.append(user)
                except ValueError:
                    print('Ignoring line', line)


def send_telegram(text):
    request.urlopen('https://api.telegram.org/bot' + BOT_TOKEN +
                    '/sendMessage?' +
                    'chat_id=' + CHAT_ID +
                    '&text=' + text
                    )


if __name__ == '__main__':
    BOT_TOKEN = sys.argv[1]
    CHAT_ID = sys.argv[2]
    GROUP_NAME = sys.argv[3]
    MEETUP_USERS = []

    send_telegram("Hello! I'm up and running")

    init_meetup_users(MEETUP_USERS)
    if len(MEETUP_USERS) == 0:
        print('No users provided, aborting')
        send_telegram('No users provided, aborting')
        exit(0)

    events = {}

    while True:
        j = json.loads(request.urlopen('https://api.meetup.com/' +
                                       GROUP_NAME +
                                       '/events?' +
                                       'sign=true&key=' + MEETUP_USERS[0].api_key +
                                       '&fields=rsvp_rules' +
                                       '&scroll=next_upcoming'
                                       ).read())

        for event in j:
            event_id = event['id']
            t = datetime.datetime.fromtimestamp(event['time']/1000).strftime('%Y-%m-%d %H:%M:%S')

            print(t)

            if 'Football' in event['name'] and event_id not in events.keys() and '13:' in t:
                events[event_id] = event

        for key in events:
            print(events[key])
            t = datetime.datetime.fromtimestamp(events[key]['time']/1000).strftime('%Y-%m-%d %H:%M:%S')
            send_telegram("I'm trying to rsvp to " + events[key]['name'] + " on " + t + ". I'll let you know when I have any updates :)")

            for user in MEETUP_USERS:
                rsvped = False
                url = 'https://api.meetup.com/' + GROUP_NAME + '/events/' + key + '/rsvps?sign=true&key=' + user.api_key + '&response=yes'

                while not rsvped:
                    try:
                        req = request.Request(url)
                        d = parse.urlencode({}).encode()
                        j = request.urlopen(req, data=d)
                        if j.getcode() == 201 or j.getcode() == '201':
                            rsvped = True
                            send_telegram('I just registered ' + user.name + ' to ' + events[key]['name'] + ' on ' + str(t))
                    except Exception as error:
                        print(error)
                        time.sleep(300)


        send_telegram("I don't have any more events, stop being lazy and write better code!!!")
        break
