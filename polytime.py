import datetime
import time
import argparse
import re
import json

def loadConfig():
    try:
        with open('config') as f:
            conf = json.loads(f.read())
            return conf

    except (FileNotFoundError, ValueError) as e:
        return 0

def loadArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sleeps', nargs='+',
            help='Enter a series of time ranges (e.g. "--sleeps 01:30-02:00 03:00-04:25"). Optionally add names prior to any or all of the ranges to name them (e.g. "--sleeps Alpha 05:30-07:00 Beta 12:00-12:20 Gamma 16:00-16:20 Delta 22:00-01:00").')
    parser.add_argument('-dm', '--dateMultiplier', action='store_true', help='This replaces the days in the date with the number of arcs since the start of the month.')
    return parser.parse_args()

def saveConfig(conf):
    with open('config', 'w') as f:
        f.write(json.dumps(conf, indent=4))

# configurator for user input
# each parameter needs a ratching loadArgs() entry
def configurator():
    # Loading the config
    conf = loadConfig()
    if conf == 0:
        conf = json.loads('{}')

    # Loading the command line arguments
    args = loadArgs()

    # Sleep time config check
    if args.sleeps is not None:
        pattern = re.compile('^\d{2}:\d{2}-\d{2}:\d{2}$')
        nameCache = ''
        sleepCache = json.loads('{"sleeps": []}')

        for i in range(len(args.sleeps)):
            if re.search(pattern, args.sleeps[i]):
                sleep = json.loads('{"name": "", "start": "", "end": ""}')
                if nameCache != '':
                    sleep['name'] = nameCache

                times = args.sleeps[i].replace('-', ' ').replace(':', '').split()
                sleep['start'] = times[0]
                sleep['end'] = times[1]
                
                sleepCache['sleeps'].append(sleep)

                nameCache = ''
                continue

            nameCache = args.sleeps[i]

        if sleepCache['sleeps'] != []:
            conf['sleeps'] = sleepCache['sleeps']

        args.sleeps = None
    elif 'sleeps' not in conf:
        conf['sleeps'] = json.loads('[{"name": "", "start": "0000", "end": "0000"}]')

    for sleep in conf['sleeps']:
        pass
        
    # Date multiplier config check
    if 'dateMultiplier' not in conf:
        conf['dateMultiplier'] = json.loads('0')

    elif args.dateMultiplier is not False:
        if conf['dateMultiplier'] == 0:
            conf['dateMultiplier'] = 1
        else:
            conf['dateMultiplier'] = 0
    
    # Save the latest version of the config
    saveConfig(conf)

    # Convert human readable config to a useful config
    loadTime(conf)
    print(json.dumps(conf, indent=4))
    #runTime(conf, conf['dateMultiplier'])

# Load sleep times
def loadTime(conf):
    # The solution here seems to be to have an alternate new imitation of conf['sleeps'], that then replaces conf['sleeps']
    newSleeps = json.loads('[]')

    for sleep in conf['sleeps']:
        newSleep = sleep.copy()
        newSleep['start'] = int(newSleep['start'][:2]) * 3600 + int(newSleep['start'][2:]) * 60
        newSleep['end'] = int(newSleep['end'][:2]) * 3600 + int(newSleep['end'][2:]) * 60

        if newSleep['start'] > newSleep['end']:
            newSleep2 = newSleep.copy()
            newSleep['end'] += 86400
            newSleep2['start'] -= 86400
            newSleeps.append(newSleep2)

        newSleeps.append(newSleep)

    conf['sleeps'] =  sorted(newSleeps, key=lambda tup: tup['start'])
    return

def runTime(timings, multiplier):
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0)
    nowS = (now - midnight).total_seconds()
    for time in range(len(timings)):
        print('runtime:', timings[time][2], nowS, timings[time][2])
        if nowS > timings[time][2] and nowS < timings[time + 1][2]:
            time = (datetime.datetime.now() - datetime.timedelta(seconds=timings[time - 1][2]))
            


            print('{0}-{1:02d}-{2} | {3:02d}:{4:02d}:{5:02d} {6}'.format(time.year, time.month, dateDays, time.hour, time.minute, dateSeconds, sleepsIn[currentArc][0]))
        
## conversion of sleep times to second based values and sorting
#def sleepTimes(input):
#    arcs = []
#    for i in range(len(input)):
#        start = (int(input[i][1][0])*3600)+(int(input[i][1][1])*60)
#        end = (int(input[i][1][2])*3600)+(int(input[i][1][3])*60)
#        arcs.append([input[i][0], start, end])
#    arcs = sorted(arcs, key=lambda tup: tup[2])
#    return arcs
#
## function to determine the current arc
#def getArc(sleepsIn):
#    now = datetime.datetime.now()
#    midnight = now.replace(hour=0, minute=0, second=0)
#    dayEnd = 86400
#    nowS = (now - midnight).total_seconds()
#    if nowS > 0 and nowS < sleepsIn[0][2]:
#        return 1
#
#    if nowS < dayEnd and nowS > sleepsIn[-1][2]:
#        return 0
#
#    for i in range(len(sleepsIn)):
#        if nowS > sleepsIn[i-1][2] and nowS < sleepsIn[i][2]:
#            return i
#
## print the current polytime, with date and arc name
#def printTime(sleepsIn):
#    currentArc = getArc(sleepsIn)
#    time = (datetime.datetime.now() - datetime.timedelta(seconds=sleepsIn[currentArc - 1][2]))
#
#    dateDays = time.day
#    if args.dateMultiplier is True:
#        if currentArc > 0:
#            dateDays = (time.day - 1) * len(sleepsIn) + currentArc
#        else:
#            dateDays = (time.day - 1) * len(sleepsIn) + len(sleepsIn)
#
#    dateSeconds = time.second
#    if (dateSeconds % 10) < 5:
#        dateSeconds = dateSeconds - (dateSeconds % 10)
#    else:
#        dateSeconds = dateSeconds - (dateSeconds % 10) + 5
#
#    print('{0}-{1:02d}-{2} | {3:02d}:{4:02d}:{5:02d} {6}'.format(time.year, time.month, dateDays, time.hour, time.minute, dateSeconds, sleepsIn[currentArc][0]))
#
configurator()
