import csv
import os
import platform
from pprint import pprint
from collections import namedtuple


def toggl():
    sheet = get_latest_sheet()
    pprint(f'todays timesheet is {sheet}')
    Event = namedtuple('Event', ['tags', 'duration', 'task', 'description', 'start'])
    unique_day = {}
    with open(sheet, 'r') as reader:
        reader = csv.DictReader(reader)
        for row in reader:
            event = Event(row['Tags'], convert_duration(row['Duration']), row['Task'],
                          row['Description'], row['Start date'])
            item = event[-1] + '-' + event[0] if len(event[0]) > 1 else \
                event[-1] + '-' + 'general admin'
            if item in unique_day:
                # add to duration
                unique_day[item] += event[1]
            else:
                unique_day[item] = event[1]

        pprint(unique_day)


def convert_duration(duration):
    """Toggle exports duration as a string like '3:30:00'
        This converts it to a float like '3.5'
        return: float rounded to 2 decimal places"""
    h, m, s = duration.split(':')
    total_secs = int(h) * 3600 + int(m) * 60 + int(s)
    # If you want more precise 2 digit time return hours
    hours = round(total_secs / 3600, 2)
    # otherwise return this sweet quarter hour round
    round_quarter_hour = round(hours * 4) / 4
    return round_quarter_hour


def get_latest_sheet():
    downloads = os.path.join(os.path.expanduser('~'), 'Downloads/')
    toggl_files = [x for x in os.listdir(downloads) if x.startswith("Toggl")]
    sheet = get_most_recent_file(downloads, toggl_files)
    return downloads + sheet  # Full path to sheet


def get_most_recent_file(downloads, toggl_files):
    """returns oldest file in a list"""
    times = {}
    for i in toggl_files:
        times[i] = os.path.getctime(downloads + i)

    return max(times, key=times.get)


if __name__ == "__main__":
    pprint(f'os name: {os.name}')
    pprint(f'platform: {platform.system()}')
    toggl()

