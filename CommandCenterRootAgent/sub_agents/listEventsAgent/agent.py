
from google.adk.agents import Agent
from ...tools.tools import csv_tool


list_events_agent = Agent(
    model='gemini-1.5-pro',
    name='ListEventsAgent',
    description='Displays a table of all current events.',
    instruction='''
Use csv_tool with action="read" to load all events from the event log.
Present the results in a markdown table format.

The table must include the following columns (with Hebrew headers):
- מזהה אירוע (event_id)
- שם אירוע (event_name)
- סוג אירוע (event_type)
- מצב (status)
- פצועים (injured)
- נ"צ (location)

Only show events that have status = "פתוח".
If no events found, respond with: "אין אירועים פתוחים במערכת."
Return all events in a markdown table with proper formatting.

Make sure to include:
| מזהה אירוע | שם אירוע | סוג אירוע | מצב | פצועים | נ"צ |
|------------|----------|------------|------|----------|------|
| ...        | ...      | ...        | ...  | ...      | ...  |

Each row must be aligned with pipes `|` and include the separator row.
the colomns is only for the demonstration 
dont combine uuid and english in your response
''',
    tools=[csv_tool]
)