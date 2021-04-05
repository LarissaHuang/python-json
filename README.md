# Event Organizer with Python and JSON

## Getting Started

This Python script checks the availability of team members over the course of one working day, returning the participants that are available for a meeting, and those who cannot attend.

### Prerequisites

python 3
pip3
Flask

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

Your localhost home route should be 127.0.0.1:5000/. You should see the schedule of all participants captured here.


To test a potential meeting time, enter the following in the URL field, passing in date and duration fields in the URL:

```
127.0.0.1:5000/api/availability?date=2021-01-01&duration=30
```

You should be able to see all the participants that can attend in each time slot's participants list. Those that cannotAttend due to another meeting are in the cannotAttend list. 

```
{
    "cannotAttend": [
        "Jade"
    ], 
    "endTime": "Fri, 01 Jan 2021 09:45:00 GMT", 
    "participants": [
        "Mike", 
        "Bob"
    ], 
    "startTime": "Fri, 01 Jan 2021 09:15:00 GMT"
}, 
```
Note that the order of JSON objects is alphabetical by default, therefore endTime is displayed before startTime
## Next steps

As a next step, I will be working on submitting a POST request in order to add busyBlocks by updating the schedule.json file.

