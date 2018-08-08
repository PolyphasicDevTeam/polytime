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
                sleep = json.loads('{}')
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

    if args.dateMultiplier is not False:
        if conf['dateMultiplier'] == 0:
            conf['dateMultiplier'] = 1
        else:
            conf['dateMultiplier'] = 0
    
    # Save the latest version of the config
    saveConfig(conf)

    # Convert human readable config to a useful config
    loadTime(conf)

    # Run app
    runTime(conf)

# Load sleep times
def loadTime(conf):
    # The solution here seems to be to have an alternate new imitation of conf['sleeps'], that then replaces conf['sleeps']
    newSleeps = json.loads('[]')
    
    conf['sleepCount'] = 0

    for sleep in conf['sleeps']:
        newSleep = sleep.copy()
        newSleep['start'] = int(newSleep['start'][:2]) * 3600 + int(newSleep['start'][2:]) * 60
        newSleep['end'] = int(newSleep['end'][:2]) * 3600 + int(newSleep['end'][2:]) * 60

        if newSleep['start'] > newSleep['end']:
            newSleep2 = newSleep.copy()
            newSleep['end'] += 86400
            newSleep2['start'] -= 86400
            newSleeps.append(newSleep2)
        
        conf['sleepCount'] += 1
        newSleeps.append(newSleep)

    conf['sleeps'] = sorted(newSleeps, key=lambda tup: tup['start'])

    prevSleep = 0
    for sleep in conf['sleeps']:
        sleep['prevSleep'] = prevSleep
        prevSleep = sleep['end']
    return

def runTime(conf):
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0)
    nowS = (now - midnight).total_seconds()

    arcSleep = 0
    for i in range(len(conf['sleeps'])):
        if nowS > conf['sleeps'][i]['prevSleep'] and nowS < conf['sleeps'][i]['end']:
            arcSleep = i
            break
    
    time = (datetime.datetime.now() - datetime.timedelta(seconds=conf['sleeps'][arcSleep]['prevSleep']))

    dateDays = time.day
    if conf['dateMultiplier']:
        dateDays = dateDays * conf['sleepCount'] + arcSleep

    dateSeconds = time.second
    if (dateSeconds % 10) < 5:
        dateSeconds = dateSeconds - (dateSeconds % 10)
    else:
        dateSeconds = dateSeconds - (dateSeconds % 10) + 5

    print('{0}-{1:02d}-{2} | {3:02d}:{4:02d}:{5:02d} {6}'.format(time.year, time.month, dateDays, time.hour, time.minute, dateSeconds, conf['sleeps'][arcSleep]['name']))

configurator()
