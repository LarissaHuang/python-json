import json
from datetime import datetime
from datetime import timedelta

with open("meetings.json") as f:
    meetingData = json.load(f)

with open("possibleSlots.json") as f:
    possibleSlots = json.load(f)

for meeting in meetingData["meetings"]:
    busyBlockStart = meeting["startTime"]
    busyBlockEnd = meeting["endTime"]

# looping through possible meeting times
for possibleSlot in possibleSlots["possibleSlots"]:

    possibleStart = datetime.strptime(possibleSlot["startTime"], "%b %d %Y %I:%M%p")
    possibleEnd = datetime.strptime(possibleSlot["endTime"], "%b %d %Y %I:%M%p")

    print("checking for possible meetings")

    with open("employees.json") as f:
        employeeData = json.load(f)

    maxParticipants = len(employeeData["employees"])

    # initialize potentialParticipants as 0
    potentialParticipants = 0

    # initialize position as 0, used for writing into json later
    position = 0

    # looping through each employee in the employees table
    for employee in employeeData["employees"]:
        # print("checking for employee", employee["id"])

        if potentialParticipants == maxParticipants:
            print("Good news! All employees are available for this meeting")
            break
        else:
            employeeMeetingList = employee["meetings"]

            # initialize overlap as false
            overlap = False

            # looping through each meeting in an employee's schedule
            for meetingId in employeeMeetingList:

                # looping through meetings in the meetings table
                for meeting in meetingData["meetings"]:

                    # checking to see if an employee is part of a meeting
                    if meetingId == meeting["id"]:

                        busyBlockStart = datetime.strptime(
                            meeting["startTime"], "%b %d %Y %I:%M%p"
                        )
                        busyBlockEnd = datetime.strptime(
                            meeting["endTime"], "%b %d %Y %I:%M%p"
                        )

                t = busyBlockStart

                # assuming busyBlockStart is before busyBlockEnd
                while t <= busyBlockEnd:

                    # if the potential meeting start time is during an already-booked meeting
                    if t >= possibleStart and t <= possibleEnd:

                        overlap = True
                        break

                    # increment time by 15 minutes
                    t = t + timedelta(minutes=15)

            if overlap == False:

                # if no overlap found, add employee to potential participants
                potentialParticipants += 1

                print("new participant added")

                # print(
                #     "total potential participants",
                #     potentialParticipants,
                #     "for potential meeting id",
                #     possibleSlot["id"],
                # )

                # this conditional prevents duplicate insertions of meetings into employee schedule
                if possibleSlot["id"] not in employeeMeetingList:
                    employeeMeetingList.append(possibleSlot["id"])

                # for i in employeeData:
                #     print("before adding, emp list", i)
                # employeeData[position] = employee

                employee_list = employeeData["employees"]
                employee_list[position] = employee

                for i in employeeData["employees"]:
                    print("emp list", i)
                # print("employee list ", employeeData)

                with open("employees.json", "w+") as jsonFile:
                    jsonFile.seek(0)
                    json.dump(employeeData, jsonFile)

            print(
                "total potential participants",
                potentialParticipants,
                "for potential meeting id",
                possibleSlot["id"],
            )
            #    update meeting list
        position += 1
        # find possible employees
    if potentialParticipants == 0:
        print("no possible time slot")

#    1. iterate through possible time slots
#     9-10
#     9:15-10:15

#    2. for each time slot calculate possible count
#     best_count = -1
#     if count > bestcount
#     replace bestcount and bestslot


#     3. return bestcount and bestslot
#     return list of employees