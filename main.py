#!/usr/bin/python3

import argparse
import random
import string
import sys

import bullet
import dates

from tinydb import TinyDB, Query

default_journal_path='bullet_desktapp.json'

def get_bullet(entry, future=False):
    if entry['kind'] == 'event':
        return 'o'
    elif entry['kind'] == 'note':
        return '-'
    elif entry['state'] == 'done':
        return 'x'
    elif future and entry['date'] != '':
        return '>'
    else:
        return '·'

def get_position(key):
    all_entries = journal.search(entries.key.exists())
    by_position = sorted(all_entries, key=lambda k: k['position'])

    for i in range(0, len(by_position)):
        if by_position[i]['key'] == key:
            return by_position[i]['position'], None if i == 0 else by_position[i-1]['position'], None if i == len(by_position)-1 else by_position[i+1]['position']


    return None, None, None

def new_key(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def new_position():
    if len(journal) == 0:
        return 100

    last_entry = sorted(journal.search(entries.position.exists()), key=lambda k: k['position'])[-1]
    return last_entry['position'] + 100

def new_entry(description='', kind='task', state='pending', date=''):
    key = new_key()
    while journal.search(entries.key == key):
        key = new_key()
    position = new_position()
    return {'description':description, 'kind':kind, 'state':state, 'date':date, 'key': key, 'position': position}

def reposition(command):
    if '<' in command:
        keys = command.replace(' ', '').split('<')
        if len(keys) == 2:
            target, previous, post = get_position(keys[-1])
            if previous == None:
                journal.update({'position': int(target/2)}, entries.key == keys[0])
            else:
                journal.update({'position': int((target+previous)/2)}, entries.key == keys[0])
    elif '>' in command:
        keys = command.replace(' ', '').split('>')
        if len(keys) == 2:
            target, previous, post = get_position(keys[-1])
            if post == None:
                journal.update({'position': target + 100}, entries.key == keys[0])
            else:
                journal.update({'position': int((target+post)/2)}, entries.key == keys[0])
    else:
        print('Repositioning command must include a position symbol, either: <, >')
        sys.exit(1)


parser = argparse.ArgumentParser(description='Manage a minimal digital bullet journal')
parser.add_argument(
    '-t',
    metavar='Task',
    dest='task',
    nargs='+',
    help='add a new task')
parser.add_argument(
    '-n',
    metavar='Note',
    dest='note',
    nargs='+',
    help='add a new note')
parser.add_argument(
    '-e',
    dest='event',
    nargs='+',
    help='add a new event')
parser.add_argument(
    '-d',
    metavar='YYYY-MM-DD',
    dest='date',
    nargs=1,
    help='set the date of the new/updated entry. Entries without date or an empty value are placed in the future log. Events must include a date.')
parser.add_argument(
    '-j',
    metavar='Path',
    dest='path',
    nargs=1,
    help='set an custom path to the journal file.')
parser.add_argument(
    '-x',
    metavar='Key',
    dest='done',
    nargs='+',
    help='mark a task as done')
parser.add_argument(
    '-p',
    metavar='Reposition',
    dest='reposition',
    nargs=1,
    help='move a task either before or after another')
parser.add_argument(
    '-s',
    metavar='Key [Date]',
    dest='schedule',
    nargs='+',
    help='With one argument, send entry to future log. With two arguments set date for an entry.')
parser.add_argument(
    '-l',
    action='store_true',
    help="list today's log")
parser.add_argument(
    '-f',
    action='store_true',
    help="list the future log")
parser.add_argument(
    '-m',
    action='store_true',
    help="list the monthly log. This only shows the events.")
parser.add_argument(
    '-w',
    action='store_true',
    help='list the weekly log.')
parser.add_argument(
    '-k',
    action='store_true',
    help='include the key to the entry listed.')

args = parser.parse_args()

journal = TinyDB(args.path[0] if args.path else default_journal_path)

entries = Query()

if args.schedule:
    journal.update({'date': args.schedule[1] if len(args.schedule) > 1 else ''}, entries.key == args.schedule[0])
elif args.reposition:
    reposition(args.reposition[0])
elif args.done:
    for key in args.done:
        journal.update({'state': 'done'}, entries.key == key)

        entry = journal.search(entries.key == key)
        if entry[0]['date'] == '':
            journal.update({'date': dates.get_today()}, entries.key == key)
elif args.task:
    date = '' if args.f else (args.date if args.date else dates.get_today())
    journal.insert(
        new_entry(description=' '.join(args.task),
            kind='task',
            date=date))
elif args.event:
    if not args.date:
        print("Events must include a date!")
        sys.exit(1)
    else:
        journal.insert(
            new_entry(description=' '.join(args.event),
                kind='event',
                date=args.date[0]))
elif args.note:
    journal.insert(
        new_entry(description=' '.join(args.note),
            kind='note',
            date=(args.date if args.date else dates.get_today())))
elif args.l:
    print(dates.get_today() + ':')
    for entry in sorted(journal.search(entries.date == dates.get_today()), key=lambda k: k['position']):
        with_key = ' [%s]' % entry['key'] if args.k else ''
        print(' %s %s%s' % (get_bullet(entry), entry['description'], with_key))
elif args.w:
    print("Week %d (%d): " % (dates.this_week()[1], dates.this_week()[0]))
    for entry in bullet.weekly_log(journal):
        with_key = ' [%s]' % entry['key'] if args.k else ''
        print(' %s %s%s' % (get_bullet(entry), entry['description'], with_key))
elif args.m:
    print(dates.this_month() + ':')
    for entry in bullet.monthly_log(journal):
        with_key = ' [%s]' % entry['key'] if args.k else ''
        print(' %s %s%s' % (get_bullet(entry), entry['description'], with_key))
elif args.f:
    print('Future log:')
    #for entry in sorted(bullet.future_log(journal), key=lambda k: k['position']):
    for entry in bullet.future_log(journal) + bullet.monthly_log(journal):
        with_key = ' [%s]' % entry['key'] if args.k else ''
        print(' %s %s%s' % (get_bullet(entry, future=True), entry['description'], with_key))
