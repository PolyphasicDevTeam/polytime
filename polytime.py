import datetime
import time
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('--sleeps', nargs='+',
        help='Enter a series of time ranges (e.g. "--sleeps 01:30-02:00 3:00-4:25"). Optionally add names prior to any or all of the ranges to name them (e.g. "--sleeps Alpha 05:30-07:00 Beta 12:00-12:20 Gamma 16:00-16:20 Delta 22:00-01:00").')
parser.add_argument('-dm', '--dateMultiplier', action='store_true', help="This replaces the days in the date with the number of arcs since the start of the month.")
args = parser.parse_args()

# configurator for user input
def configurator():
    sleeps = []
    pattern = re.compile("\d{2}:\d{2}-\d{2}:\d{2}")

    if args.sleeps is not None:
        nameCache = ''
        for i in range(len(args.sleeps)):
            if re.search(pattern, args.sleeps[i]):
                if nameCache == '':
                    sleeps.append([''])

                else:
                    sleeps.append([nameCache])

                sleeps[len(sleeps) - 1].append(args.sleeps[i].replace('-', ' ').replace(':', ' ').split())
                nameCache = ''
                continue

            nameCache = args.sleeps[i]
        printTime(sleepTimes(sleeps))
    else:
        printTime([['', 0, 0]])
        sleeps = ['', ['00:00-00:00']]

# conversion of sleep times to second based values and sorting
def sleepTimes(input):
    arcs = []
    for i in range(len(input)):
        start = (int(input[i][1][0])*3600)+(int(input[i][1][1])*60)
        end = (int(input[i][1][2])*3600)+(int(input[i][1][3])*60)
        arcs.append([input[i][0], start, end])
    arcs = sorted(arcs, key=lambda tup: tup[2])
    return arcs

# function to determine the current arc
def getArc(sleepsIn):
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0)
    dayEnd = 86400
    nowS = (now - midnight).total_seconds()
    if nowS > 0 and nowS < sleepsIn[0][2]:
        return 1

    if nowS < dayEnd and nowS > sleepsIn[-1][2]:
        return 0

    for i in range(len(sleepsIn)):
        if nowS > sleepsIn[i-1][2] and nowS < sleepsIn[i][2]:
            return i

# print the current polytime, with date and arc name
def printTime(sleepsIn):
    currentArc = getArc(sleepsIn)
    time = (datetime.datetime.now() - datetime.timedelta(seconds=sleepsIn[currentArc - 1][2]))

    dateDays = time.day
    if args.dateMultiplier is True:
        if currentArc > 0:
            dateDays = (time.day - 1) * len(sleepsIn) + currentArc
        else:
            dateDays = (time.day - 1) * len(sleepsIn) + len(sleepsIn)

    dateSeconds = time.second
    if (dateSeconds % 10) < 5:
        dateSeconds = dateSeconds - (dateSeconds % 10)
    else:
        dateSeconds = dateSeconds - (dateSeconds % 10) + 5

    print('{0}-{1:02d}-{2} | {3:02d}:{4:02d}:{5:02d} {6}'.format(time.year, time.month, dateDays, time.hour, time.minute, dateSeconds, sleepsIn[currentArc][0]))

configurator()
