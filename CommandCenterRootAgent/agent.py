# Multi-Agent Operational Command Center Bot (ADK)

from google.adk.agents import Agent
from .sub_agents.createEventAgent.agent import create_event_agent
from .sub_agents.updateEventAgent.agent import update_event_agent
from .sub_agents.summaryAgent.agent import summary_agent
from .sub_agents.listEventsAgent.agent import list_events_agent

# -----------------------------
# Root Agent
# -----------------------------
root_agent = Agent(
    model='gemini-1.5-pro',
    name='CommandCenterRootAgent',
    description='Main agent that routes incoming Hebrew operational requests to the appropriate sub-agent.',
    instruction='''
You are the root coordinator for a multi-agent emergency operations system.
Analyze the user's Hebrew input and delegate ONLY to one of the sub-agents listed in the "sub_agents" section.

Your task is strictly routing. You must not answer the user directly or handle business logic yourself.

Look for intent in the user's input:
- If the user reports a new emergency → delegate to create_event_agent
- If the user mentions updating or correcting information → delegate to UpdateEventAgent
- If it's ambiguous or unclear whether it's new or update → assume it is a new emergency and delegate to CreateEventAgent
- If the user requests a list or report of events →
    - If requesting a table → ListEventsAgent
    - If requesting a summary for command → SummaryAgent

Use the sub_agents block below to call the right agent.
if you didnt succes plese notufy the user that there is error
''',
    sub_agents=[create_event_agent,update_event_agent, summary_agent, list_events_agent]
)