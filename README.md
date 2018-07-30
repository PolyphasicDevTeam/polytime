# polytime
An alternative clock which splits the day into segments (each starting with a time of 00:00:00) based on one or more sleep times. 

 ```
 monika@archlinux> python polytime.py                                                                               ~/polytime
2018-07-29 | 09:28:20 
monika@archlinux> python polytime.py --sleeps Alpha 05:30-07:00 Beta 12:00-12:20 Gamma 16:00-16:20 Delta 22:00-01:00    
2018-07-29 | 02:28:20 Beta
monika@archlinux> python polytime.py --sleeps Alpha 05:30-07:00 Beta 12:00-12:20 Gamma 16:00-16:20 Delta 22:00-01:00 -dm
2018-07-114 | 02:28:20 Beta
```

# Usage
Type `python polytime -h` or `python polytime --help` for a description of currently available flags.

# Basic concept

People on monophasic sleep schedules have the convenient concept of a "day" and they sleep at the end of it, right? That way they get a proper sense of productivity relative to their wake time. With this in mind a friend of mine defined a concept of an "arc", which is the period between 2 sleeping episodes and thought of creating a program to replace day based clocks with arc based ones.

Arcs can be labeled as well, for example right now I'm on mashiro, and the end of mashiro is a nap. When mashiro ends, the clock should show "00:00:00 Hanako".

# Plans

There are multiple ways in which this concept can be expanded on. The key ideas now are:
- Elements to expand on the feeling that each arc has a distinct start and end, as well as expanding on differentiating between the arcs for the same purpose.
- Adding different ways to handle the time on each arc (e.g. simulating 24 hours by accelerating/decelerating the speed of the clock based on a given wake period, or changing the date to show the number of arcs that elapsed since the start of the month instead of days).
- Use the time based nature of the project for alarm and adaptation assistance. This could be in the form of timed events and/or events based on user activity.
