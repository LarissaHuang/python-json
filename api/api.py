import flask
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
                schedule["startTime"], "%Y-%m-%d %I:%M %p"
            )

            # print("busy block start", busyBlockStart)
            busyBlockEnd = datetime.strptime(schedule["endTime"], "%Y-%m-%d %I:%M %p")

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

        possibleSlots.append(possibleSlot)

    # print("possible slots", possibleSlots)
    final_dict = dict()
    max_parti = len(possibleSlot["cannotAttend"])

    print("final dictionary created")
    final_dict["possibleSlot"] = possibleSlots
    print(final_dict)

    return jsonify(final_dict, max_parti)


# 127.0.0.1:5000/api/schedule?start=2021-01-01%20%2009:45%20AM&end=2021-01-01%20%2010:15%20AM&name=Jade&desc=Daily%20standup


@app.route("/api/schedule", methods=["POST"])
def addBusyBlock():

    if "start" in request.args:
        start = str(request.args["start"])
    else:
        return "Error: No start field provided. Please specify a start time."

    if "end" in request.args:
        end = str(request.args["end"])
    else:
        return "Error: No end field provided. Please specify an end time."

    if "name" in request.args:
        name = str(request.args["name"])
    else:
        return "Error: No name field provided. Please specify a name."

    if "desc" in request.args:
        desc = str(request.args["desc"])
    else:
        return "Error: No desc field provided. Please specify an desc time."

    return "<h1>added successfully</h1>"

    # initialize schedule as dictionary
    schedule = dict()
    schedule["startTime"] = start
    schedule["endTime"] = end
    schedule["participants"] = name
    schedule["description"] = desc

    with open("schedule.json", "w") as f:
        scheduleData = json.load(f)

        schedule_list = scheduleData["schedule"]
        schedule_list.append(schedule)

    # TODO: find out why the append to json file does not work
    with open("schedule.json", "w+") as jsonFile:
        scheduleData = json.load(jsonFile)
        schedule_list = scheduleData["schedule"]
        schedule_list.append(schedule)
        json.dump(schedule, jsonFile)


@app.route("/", methods=["GET"])
def home():

    with open("schedule.json") as f:

        scheduleData = json.load(f)

    return jsonify(scheduleData)


app.run()
