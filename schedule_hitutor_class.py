# coding=UTF-8

import sys
import datetime
import requests

USERNAME = '{your_hitutor_username}'
PASSWROD = '{your_hitutor_password}'

def send_email(text):
    return requests.post(
        'https://api.mailgun.net/v3/sandboxb32d692d0f75420b8f6b183034325c68.mailgun.org/messages',
        auth=('api', '{API_KEY}'),
        data={'from': 'clapperboard <clapperboard@sandboxb32d692d0f75420b8f6b183034325c68.mailgun.org>',
              'to': [USERNAME],
              'subject': '[AUTO] Scheduled the English Class!',
              'text': text})

def login():
    payload = {
        't101_email': USERNAME,
        't101_password': PASSWROD
    }
    with requests.session() as c:
        c.post('http://login.hitutor.com.tw/login-action.php', data=payload)
        return c

def schedule(c, teacher, date, time, category=146416):
    date = date.strftime('%Y-%m-%d')
    time = date + ' ' + time
    payload = {
        'date': date,
        'id': category,
        'time': time,
        'teacher': int(teacher),
        'check_mobile': False
    }
    res = c.post('http://login.hitutor.com.tw/member/class-schedule-2.php', data=payload)
    if res.status_code == 200:
        # send email
        send_email(res.content)

def main(argv):
    arg_names = ['teacher', 'date', 'time', 'category']
    args = dict(zip(arg_names, argv))

    # teacher (required)
    if 'teacher' not in args:
        print('No teacher is given. Must give one teacher to continue.')
        return
    else:
        teacher = args['teacher']

    # date (option, deafult = next Friday)
    today = datetime.date.today()
    if 'date' not in args:
        date = today + datetime.timedelta(34)
    else:
        date = today + datetime.timedelta(29 + int(args['date']))

    # time (option, default = 23:00)
    if 'time' not in args:
        time = '23:00'
    else:
        time = str(args['time']) + ':00'

    # category (option, default = 146416)
    if 'category' not in args:
        category = 146416
    else:
        category = args['category']

    # login to hitutor
    req = login()

    # schedule the class
    schedule(req, teacher, date, time, category)

if __name__ == "__main__":
    main(sys.argv[1:])