import flask
from flask import request
import json


import numpy as np
from datetime import datetime, timedelta
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# sample request
# 127.0.0.1:5000/api/availability?date=2021-01-01&duration=30
@app.route("/api/availability", methods=["GET"])
def availability():

    if "date" in request.args:
        date = str(request.args["date"])
    else:
        return "Error: No date field provided. Please specify a date."

    if "duration" in request.args:
        duration = int(request.args["duration"])
    else:
        return "Error: No duration field provided. Please specify a duration."

    startDateTime = date + " 9:00 AM"
    endDateTime = date + " 5:00 PM"

    dayStart = datetime.strptime(startDateTime, "%Y-%m-%d %I:%M %p")
    dayEnd = datetime.strptime(endDateTime, "%Y-%m-%d %I:%M %p")

    interval = timedelta(minutes=15)

    meetingInterval = timedelta(minutes=duration)

    possibleStartTimes = np.arange(dayStart, dayEnd, interval).astype(datetime)

    possibleSlots = []

    best_count = -1

    bestSlot = dict()
    bestSlot["startTime"] = ""
    bestSlot["endTime"] = ""
    bestSlot["participants"] = []
    bestSlot["cannotAttend"] = []

    # if count > bestcount
    # replace bestcount and bestslot

    for possibleStartTime in possibleStartTimes:
        possibleEndTime = possibleStartTime + meetingInterval
        # initialization of dictionary
        possibleSlot = dict()
        possibleSlot["startTime"] = possibleStartTime
        possibleSlot["endTime"] = possibleEndTime
        possibleSlot["participants"] = []
        possibleSlot["cannotAttend"] = []

        print("checking for possible meeting times")

        with open("schedule.json") as f:
            scheduleData = json.load(f)

        for schedule in scheduleData["schedule"]:
            busyBlockStart = datetime.strptime(
                schedule["startTime"], "%Y-%m-%d  %I:%M %p"
            )

            # print("busy block start", busyBlockStart)
            busyBlockEnd = datetime.strptime(schedule["endTime"], "%Y-%m-%d  %I:%M %p")

            # initialize overlap as false
            overlap = False

            print("begin overlap check")
            t = busyBlockStart
            while t <= busyBlockEnd:
                #   if t >= possibleStart and t <= possibleEnd:
                if t >= possibleStartTime and t <= possibleEndTime:
                    overlap = True
                    possibleSlot["cannotAttend"].append(schedule["participants"])
                    print(
                        "this person is busy for time block of",
                        possibleStartTime,
                        possibleEndTime,
                    )
                    print("this person added to the cannotAttend list")
                    break

                # increment time by 15 minutes
                t = t + timedelta(minutes=15)
            print("after overlap check")
            if overlap == False:
                print("employee added in participants list")

                possibleSlot["participants"].append(schedule["participants"])

            count = len(possibleSlot["participants"])

            if count > best_count:
                bestSlot = possibleSlot
                best_count = count

            possibleSlots.append(possibleSlot)

    # print("possible slots", possibleSlots)
    final_dict = dict()
    max_parti = len(possibleSlot["cannotAttend"])

    print("final dictionary created")
    final_dict["possibleSlot"] = possibleSlots
    print(final_dict)

    with open("bestSlot.json", "r") as f:
        bestSlotData = json.load(f)

    final_best_slot = dict()
    final_best_slot["best_slot"] = bestSlot

    with open("bestSlot.json", "w") as f:
        json.dump(bestSlotData, f)

    return jsonify(final_dict, bestSlot)


# Finding best slot


# 127.0.0.1:5000/api/schedule?start=2021-01-01%20%2009:45%20AM&end=2021-01-01%20%2010:15%20AM&name=Jade&desc=Daily%20standup


@app.route("/api/schedule", methods=["GET", "POST"])
def addBusyBlock():

    # import urllib.request

    # webUrl = urllib.request.urlopen("/api/schedule")

    # initialize schedule as dictionary
    schedule = dict()
    schedule["startTime"] = "2021-01-01  9:45 AM"
    schedule["endTime"] = "2021-01-01  10:45 AM"
    schedule["participants"] = "Mo"
    schedule["description"] = "another standup"

    with open("schedule.json", "r") as f:
        scheduleData = json.load(f)

    schedule_list = scheduleData["schedule"]
    schedule_list.append(schedule)
    scheduleData["schedule"] = schedule_list

    with open("schedule.json", "w+") as jsonFile:
        json.dump(scheduleData, jsonFile)

    return jsonify(scheduleData)


@app.route("/", methods=["GET"])
def home():

    with open("schedule.json") as f:

        scheduleData = json.load(f)

    return jsonify(scheduleData)


app.run()
