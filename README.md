# Event Organizer with Python and JSON

## Getting Started

This Python script checks the availability of team members over the course of one working day, returning the participants that are available for a meeting, and those who cannot attend.

It also returns the best slot for a potential meeting, as defined by having the maximum number of participants. 

The best slot can then be added to the schedule as a meeting. 

### Prerequisites
```
python 3
pip3
Flask
```

Be sure to have Flask installed with 

```
pip3 install flask
```

### Running the code locally

Navigate to the api folder with

```
cd api
```

Run the app using
```
python3 api.py
```

Your localhost home route should be 127.0.0.1:5000/. You should see all booked meetings here.


To test a potential meeting time, enter the following in the URL field, passing in date and duration fields in the URL:

```
127.0.0.1:5000/api/availability?date=2021-01-01&duration=30
```

You should be able to see all the participants that can attend in each time slot's participants list. Those that cannotAttend due to another meeting are in the cannotAttend list. 

```
{
    "startTime": "Fri, 01 Jan 2021 09:15:00 GMT", 
    "endTime": "Fri, 01 Jan 2021 09:45:00 GMT", 
    "participants": [
        "Jade", 
        "Bob", 
        "Larissa"
    ], 
    "cannotAttend": [
        "Mike"
    ]
}, 

```
Below the "possibleSlots" JSON object, we can see the best slot: 

```
  "best slot", 
  {
    "startTime": "Fri, 01 Jan 2021 09:00:00 GMT", 
    "endTime": "Fri, 01 Jan 2021 09:30:00 GMT", 
    "participants": [
      "Mike", 
      "Jade", 
      "Bob", 
      "Larissa"
    ], 
    "cannotAttend": []
  }
  ```

## Posting a Busy Block

We can POST a busyBlock in the schedule by passing the values from the best slot  through the URL like so: 

```

127.0.0.1:5000/api/schedule?startTime=2021-01-01T09:00:00&endTime=2021-01-01T09:30:00&name=Larissa&description=Intro%20standup
```

We can see the block we just added underneath "Added data", and also in the bottom of the schedule list. If you open the schedule.json file in the project folder, you will also see this entry added.

## Checking the calendar

Now, when we return to the home route at 127.0.0.1:5000/, we can see a list of the updated meetings schedule, with the newly added busy block.


