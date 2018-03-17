import json
import datetime
import time
import sys
from urllib import request, parse


API_KEY = ''
GROUP_NAME = ''
EVENT_FILTER = ''
BOT_TOKEN = ''
CHAT_ID = ''


def send_telegram(text):
    request.urlopen('https://api.telegram.org/bot' + BOT_TOKEN +
                    '/sendMessage?' +
                    'chat_id=' + CHAT_ID +
                    '&text=' + text
                    )

if __name__ == '__main__':
    TOKEN = sys.argv[1]
    API_KEY = sys.argv[2]
    CHAT_ID = sys.argv[3]
    GROUP_NAME = sys.argv[4]

    events = {}

    send_telegram("Hello! I'm up and running")

    while True:
        j = json.loads(request.urlopen('https://api.meetup.com/' +
                                       GROUP_NAME +
                                       '/events?' +
                                       'sign=true&key=' + API_KEY +
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
            rsvped = False
            print(events[key])
            t = datetime.datetime.fromtimestamp(events[key]['time']/1000).strftime('%Y-%m-%d %H:%M:%S')
            send_telegram("I'm trying to rsvp to " + events[key]['name'] + " on " + t + ". I'll let you know when I have any updates :)")

            url = 'https://api.meetup.com/' + GROUP_NAME + '/events/' + key + '/rsvps?sign=true&key=' + API_KEY + '&response=yes'

            while not rsvped:
                try:
                    req = request.Request(url)
                    d = parse.urlencode({}).encode()
                    j = request.urlopen(req, data=d)
                    if j.getcode() == 201 or j.getcode() == '201':
                        rsvped = True
                        send_telegram('I just registered you to ' + events[key]['name'] + ' on ' + str(t))
                except Exception as error:
                    print(error)
                finally:
                    time.sleep(300)

        send_telegram("I don't have any more events, stop being lazy and write better code!!!")
        break
