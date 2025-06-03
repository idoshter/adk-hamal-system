from google.adk.agents import Agent
from ...tools.tools import csv_tool,notify_tool




create_event_agent = Agent(
    model='gemini-1.5-pro',
    name='CreateEventAgent',
    description='Creates a new operational event and appends it to a CSV log.',
    instruction='''
You are responsible for registering a new emergency event in Hebrew.

Steps:
1. Extract the following fields:
- event_id: generate one if not provided (only the tool )
Do NOT generate the event_id yourself.
Let the tool create the ID automatically.
- event_name: short Hebrew title based on context
- event_description: use the full original user text
- event_type: one of ["רקטה", "טיל", "שריפה", "רעידת אדמה"]
- injured / dead: numbers, or leave blank
- rescue_required: "כן" or "לא"
- status: "פתוח"
- location: extract location name if present, else leave blank
- event_time: if not mentioned, set to current timestamp
- urgency: detect from text → "דחוף" / "לא דחוף" or leave blank
- area_type: if mentioned as "בנוי" or "פתוח", use it. Else, leave blank
- damage_level: extract only if explicitly mentioned, otherwise leave blank

2. Use csv_tool with action="write" to save the event

3. Use notify_tool with the event_type, injured and rescue_required fields.
It should return one or two messages, such as:
- "נשלחה הודעה למד"א"
- "נשלחה הודעה לכיבוי והצלה"

At the end, respond to the user with:
- Confirmation line: "אירוע חדש נרשם בהצלחה במערכת. מספר מזהה: <event_id>"
- On next lines, the results of notify_tool (if any)
- Each line must be separate namely in new line. 

Do not wait for clarification. Perform all actions and return the response immediately.
After completing the update and notifications, return a final response to the user.
Do not delegate or transfer again.
''',
    tools=[csv_tool, notify_tool]
)