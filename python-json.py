import json
import datetime

with open("meetings.json") as f:
    meetingData = json.load(f)

with open("employees.json") as f:
    employeeData = json.load(f)

with open("possibleSlots.json") as f:
    possibleSlots = json.load(f)

totalEmployees = len(employeeData["employees"])

for meeting in meetingData["meetings"]:
    # print(meeting["participants"], meeting["description"])
    d = meeting["description"]
    p = meeting["participants"]
    meetingStart = meeting["startTime"]
    meetingEnd = meeting["endTime"]

    allParticipants = len(p)
    print("number of participants " + str(allParticipants))

# print("total emps" + str(totalEmployees))

for employee in employeeData["employees"]:
    # print(employee["id"])
    y = employee["id"]
    n = employee["name"]


for possibleSlot in possibleSlots["possibleSlots"]:
    # print(employee["id"])
    possibleStart = possibleSlot["startTime"]
    possibleEnd = possibleSlot["endTime"]

    print(meetingStart)

    if meetingStart > possibleStart and meetingEnd < possibleStart:
        print("possible meeting")

    # people who are busy
    y in p
    print(n + " is busy")

    # people who are free
    y not in p
    print(n + " is free")
    print("add to " + n + "'s calender")