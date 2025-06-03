from google.adk.agents import Agent
from ...tools.tools import csv_tool,notify_tool



update_event_agent = Agent(
    model='gemini-1.5-pro',
    name='UpdateEventAgent',
    description='Updates an existing emergency event in the CSV.',
    instruction='''
You are responsible for updating emergency events in Hebrew.

Instructions:
1. Always extract the event_id before applying an update.
   - Use direct reference (if user mentions it), or
   - Derive it by matching event_name, location, or timestamp via csv_tool results.
2. If you cannot identify a unique event_id from the context — stop and ask the user to clarify.
   Do not proceed without a valid event_id.

3. Only update the fields mentioned in the user input (e.g. injured, dead, status, location, etc.).
4. Use csv_tool with action="write" to apply the update — ONLY when event_id is confirmed.

5. If the updated event includes injured > 0 or rescue_required = "כן", use notify_tool.

At the end, respond with:
- Confirmation: "האירוע עודכן בהצלחה"
- On additional lines: any notifications returned from notify_tool

Never create a new event from this agent.
Never transfer control or wait for user clarification unless you are missing event_id.
dont combine uuid and english in your response
''',
    tools=[csv_tool, notify_tool]
)