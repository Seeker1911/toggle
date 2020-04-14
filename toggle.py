import csv
import os


def toggl():
    sheet = get_latest_sheet()
    with open(sheet, 'r') as reader:
        reader = csv.DictReader(reader)
        print(reader)


def get_latest_sheet():
    downloads = os.path.join(os.path.expanduser('~'), 'Downloads/')
    toggl_files = [x for x in os.listdir(downloads) if x.startswith("Toggl")]
    sheet = get_most_recent_file(downloads, toggl_files)
    
    return downloads + sheet


def get_most_recent_file(downloads, toggl_files):
    """returns oldest file in a list"""
    times = {}
    for i in toggl_files:
        times[i] = os.path.getctime(downloads + i)

    return min(times, key=times.get)


if __name__ == "__main__":
    toggl()
