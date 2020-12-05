from pprint import pprint
import time
from datetime import datetime, timedelta
import os
import re
from collections import Counter


class ShiftEntry():
    WAKEUP = 0
    GOTOSLEEP = 1
    NEWGUARD = 2

    def __init__(self, inputString, *args, **kwargs):
        # [1518-10-27 00:55] wakes up
        self.matchRegex = r"\[(.+)\] (.*)"
        matches = re.match(self.matchRegex, inputString)
        try:
            self.timeStamp, self.Command = matches.groups()
        except:
            raise "Malformed data"
        self.time = datetime.strptime(self.timeStamp, "%Y-%m-%d %H:%M",)
        # pprint(self.time)

    def commandType(self):
        if self.Command == "falls asleep":
            return self.GOTOSLEEP
        elif self.Command == "wakes up":
            return self.WAKEUP
        else:
            return self.NEWGUARD

    def getGuardIdOrNone(self):
        Gid = re.match(r"Guard #([0-9]+)", self.Command)
        return Gid.group(1)

    def __str__(self):
        return f"{time.strftime(self.timeStamp)} - {self.Command}"


def minuteRange(minTime1, minTime2):
    curMin = minTime1
    while(curMin != minTime2):
        yield curMin
        curMin = (curMin + 1) % 60


if __name__ == "__main__":
    shiftEntries = []
    with open("day4.input") as inp:
        for i in inp:
            shiftEntries += [ShiftEntry(i)]

    shiftEntries.sort(key=lambda se: se.timeStamp)

    guardSleepTime = Counter()
    asleepTime = datetime.now()
    currentGuard = 0
    guards = {}
    g3041Counter = Counter()

    for i in shiftEntries:
        typ = i.commandType()
        if typ == ShiftEntry.NEWGUARD:
            currentGuard = i.getGuardIdOrNone()
            if currentGuard not in guards:
                guards[currentGuard] = Counter()
        elif typ == ShiftEntry.GOTOSLEEP:
            asleepTime = i.time
        elif typ == ShiftEntry.WAKEUP:
            timeAsleep = i.time - asleepTime
            guardSleepTime[currentGuard] += (timeAsleep.seconds // 60)
            asleepMin = asleepTime.minute
            awakeMin = i.time.minute
            for minute in minuteRange(asleepMin, awakeMin):
                guards[currentGuard][minute] += 1
            if currentGuard == "3041":
                for minute in minuteRange(asleepMin, awakeMin):
                    g3041Counter[minute] += 1
    minutes = {}
    for i in range(00, 59):
        minutes[i] = Counter()
    print(guardSleepTime.most_common())
    print(g3041Counter.most_common())
