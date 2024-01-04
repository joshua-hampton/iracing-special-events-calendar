# iracing-special-events-calendar
ics Calendar containing iRacing special events

## Subscribe to calendar
In your calendar app of choice, there should be an option to add a calendar similar to "Subscribe from web", and use the following URL:
https://raw.githubusercontent.com/joshua-hampton/iracing-special-events-calendar/main/calendars/iracing_special_events.ics

## Contribute
While I will attempt to keep this up to date, I might miss things, mis-type bits, or just be too busy to notice updates from iRacing. 
Each special event is represented in a yaml file, the minimum information needed is the name, the start and end date, the iteration key, and a text description.
The "iteration" key must be equal to 0 for new events, and incremented each time that event is changed.

To run the code to create the calendar, first make sure the python requirements are installed, and then run the bash script. 
Note, Python 3.12 or newer is required.
