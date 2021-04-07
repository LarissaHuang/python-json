import flask
from flask import request
import json


import numpy as np
from datetime import datetime, timedelta
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def _find_availability(date, duration):
    # if "date" in request.args:
    #     date = str(request.args["date"])
    # else:
    #     return "Error: No date field provided. Please specify a date."
    #
    # if "duration" in request.args:
    #     duration = int(request.args["duration"])
    # else:
    #     return "Error: No duration field provided. Please specify a duration."

    startDateTime = date + " 9:00 AM"
    endDateTime = date + " 5:00 PM"

    dayStart = datetime.strptime(startDateTime, "%Y-%m-%d %I:%M %p")
    dayEnd = datetime.strptime(endDateTime, "%Y-%m-%d %I:%M %p")

    interval = timedelta(minutes=15)

    meetingInterval = timedelta(minutes=duration)

    possibleStartTimes = np.arange(dayStart, dayEnd, interval).astype(datetime)

    possibleSlots = []

    # initialize best_count as -1
    best_count = -1

    bestSlot = dict()
    bestSlot["startTime"] = ""
    bestSlot["endTime"] = ""
    bestSlot["participants"] = []
    bestSlot["cannotAttend"] = []

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

            if possibleSlot not in possibleSlots:
                possibleSlots.append(possibleSlot)

    # print("possible slots", possibleSlots)
    final_dict = dict()

    print("final dictionary created")
    final_dict["possibleSlots"] = possibleSlots
    print(final_dict)

    with open("bestSlot.json", "r") as f:
        bestSlotData = json.load(f)

    final_best_slot = dict()
    final_best_slot["best_slot"] = bestSlot

    with open("bestSlot.json", "w") as f:
        json.dump(bestSlotData, f)

    return final_dict, bestSlot


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

    final_dict, bestSlot = _find_availability(date, duration)

    return jsonify("possible slots", final_dict, "best slot", bestSlot)


# 127.0.0.1:5000/api/schedule?start=2021-01-01%20%2009:45%20AM&end=2021-01-01%20%2010:15%20AM&name=Jade&desc=Daily%20standup
@app.route("/api/schedule", methods=["GET", "POST"])
def addBusyBlock():
    data = request.args
    print("data", data)

    # initialize schedule as dictionary
    schedule = dict()
    schedule["startTime"] = data["start"]
    schedule["endTime"] = data["end"]
    schedule["participants"] = data["name"]
    schedule["description"] = data["desc"]

    with open("schedule.json", "r") as f:
        scheduleData = json.load(f)

    schedule_list = scheduleData["schedule"]

    if schedule not in schedule_list:
        schedule_list.append(schedule)
        scheduleData["schedule"] = schedule_list

    with open("schedule.json", "w+") as jsonFile:
        json.dump(scheduleData, jsonFile)

    date = None
    duration = None
    bestSlot = None
    if "date" in request.args:
        date = str(request.args["date"])
    if "duration" in request.args:
        duration = int(request.args["duration"])
    if date and duration:
        final_dict, bestSlot = _find_availability(date, duration)

    if bestSlot:
        return jsonify(
            "Added data:", schedule, "All data", scheduleData, "Best Slot", bestSlot
        )
    return jsonify("Added data:", schedule, "All data", scheduleData)


@app.route("/", methods=["GET"])
def home():

    with open("schedule.json") as f:

        scheduleData = json.load(f)

    return jsonify(scheduleData)


app.run()