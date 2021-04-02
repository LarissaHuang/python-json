import json
import datetime
from datetime import datetime
from datetime import timedelta

with open("meetings.json") as f:
    meetingData = json.load(f)


# write
#     with open("replayScript.json", "w") as jsonFile:
#     json.dump(data, jsonFile)

with open("possibleSlots.json") as f:
    possibleSlots = json.load(f)

# totalEmployees = len(employeeData["employees"])

for meeting in meetingData["meetings"]:
    # print(meeting["participants"], meeting["description"])
    d = meeting["description"]

    bookedMeetingStart = meeting["startTime"]
    bookedMeetingEnd = meeting["endTime"]

    # print("number of participants " + str(allParticipants))

# print("total emps" + str(totalEmployees))

# for employee in employeeData["employees"]:
#     # print(employee["id"])
#     y = employee["id"]
#     n = employee["name"]
#     m = employee["meetings"]

max_part_list = 3

for possibleSlot in possibleSlots["possibleSlots"]:
    # print(employee["id"])
    curr_part_list = 0

    possibleStart = datetime.strptime(possibleSlot["startTime"], "%b %d %Y %I:%M%p")
    possibleEnd = datetime.strptime(possibleSlot["endTime"], "%b %d %Y %I:%M%p")

    print("checking for possible meetings")

    with open("employees.json") as f:
        employeeData = json.load(f)

    position = 0
    for employee in employeeData["employees"]:
        print("checking for employee", employee["id"])
        # print("curr_parts", curr_part_list)

        if curr_part_list == max_part_list:
            print("max participants reached")
            break
        else:
            meeting_list = employee["meetings"]
            overlap = False

            # print(meeting_list)

            for meeting_id in meeting_list:
                # print("meeting id", meeting_id)
                for meeting in meetingData["meetings"]:
                    if meeting_id == meeting["id"]:

                        bookedMeetingStart = datetime.strptime(
                            meeting["startTime"], "%b %d %Y %I:%M%p"
                        )
                        bookedMeetingEnd = datetime.strptime(
                            meeting["endTime"], "%b %d %Y %I:%M%p"
                        )
                        # break

                t = bookedMeetingStart

                while t <= bookedMeetingEnd:
                    if t >= possibleStart and t <= possibleEnd:
                        # print("not possible meeting")
                        overlap = True
                        break
                    t = t + timedelta(minutes=15)

                # print("reached overlap")
            if overlap == False:
                curr_part_list += 1
                print("new participant added")
                meeting_list.append(possibleSlot["id"])

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

            #    update meeting list

        position += 1
        # find possible employees
    if curr_part_list == 0:
        print("no possible time slot")
    # booked meeting 10-11
    # possible meeting 3-4
    # people who are busy
    # y in p
    # print(n + " is busy")

    # # people who are free
    # y not in p
    # print(n + " is free")
    # print("add to " + n + "'s calender")

#    1. iterate through possible time slots
#     9-10
#     9:15-10:15

#    2. for each time slot calculate possible count
#     best_count = -1
#     if count > bestcount
#     replace bestcount and bestslot


#     3. return bestcount and bestslot
#     return list of employees