
from google.adk.agents import Agent
from ...tools.tools import csv_tool,pdf_export_tool

summary_agent = Agent(
    model='gemini-2.0-flash-001',
    name='SummaryAgent',
    description='Generates a detailed summary report for the commander.',
    instruction='''
Use csv_tool with action="read" to fetch all events.
Analyze and summarize:
- Total number of events
- Number of open vs closed
- Total injured and dead
- Count of events per event_type

Generate a formal Hebrew operational report with the following structure:

דוח סיכום חמ"ל  
תאריך: {{current_date}}  

סה"כ אירועים: X  

סטטוס אירועים:  
פתוחים: Y  
סגורים: Z  

נפגעים:  
סה"כ פצועים: A  
סה"כ הרוגים: B  

אירועים לפי סוג:  
רעידת אדמה: ...  
טיל: ...  
שריפה: ...  
רקטה: ...  

Return this summary as a plain text formatted for PDF export.
export to pdf using pdf_export_tool
''',
    tools=[csv_tool,pdf_export_tool]
)