import csv, os, uuid
from datetime import datetime
from fpdf import FPDF

CSV_PATH = "events_log.csv"
CSV_FIELDS = [
    "event_id", "event_name", "event_description", "event_type",
    "injured", "dead", "rescue_required", "status", "location",
    "event_time", "urgency", "area_type", "damage_level"
]

def csv_tool(action: str, data: dict = {}) -> str:
    """
    Tool for reading or writing emergency events from/to CSV.

    Parameters:
    - action: 'read' or 'write'
    - data: dict containing event fields if action='write'

    Returns:
    - str: formatted response
    """
    if action == "read":
        return read_events()
    elif action == "write":
        return write_event(data)
    else:
        return "Unsupported action. Use 'read' or 'write'."

def read_events() -> str:
    if not os.path.exists(CSV_PATH):
        return "No events logged yet."
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        events = list(reader)
        if not events:
            return "No events found."
        return str(events)

def write_event(data: dict) -> str:
    # Add timestamp if missing
    if not data.get("event_time"):
        data["event_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # If no event_id provided — this is a new event
    is_new = not data.get("event_id")
    if is_new:
        data["event_id"] = str(uuid.uuid4())

    updated = False
    rows = []

    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["event_id"] == data["event_id"]:
                    row.update({k: v for k, v in data.items() if v})
                    updated = True
                rows.append(row)

    with open(CSV_PATH, 'w' if updated else 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, quoting=csv.QUOTE_ALL)
        if not os.path.exists(CSV_PATH) or os.stat(CSV_PATH).st_size == 0:
            writer.writeheader()
        if updated:
            writer.writerows(rows)
        else:
            writer.writerow(data)

    if updated:
        return f"אירוע עודכן בהצלחה. מזהה: {data['event_id']}"
    else:
        return f"אירוע חדש נוסף. מזהה: {data['event_id']}"

    
def notify_tool(event_type: str = "", injured: int = 0, rescue_required: str = "לא") -> str:
    '''
    Send alerts to MDA or Fire Department based on event details.
    '''
    messages = []
    if injured and injured > 0:
        messages.append("נשלחה הודעה למד\"א")
    if event_type == "שריפה" or rescue_required.strip() == "כן":
        messages.append("נשלחה הודעה לכיבוי והצלה")
    return "\n".join(messages)


def pdf_export_tool(report_text: str) -> str:
    '''
    Export a given Hebrew report to PDF and return filename.
    '''
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Arial', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
    pdf.set_font("Arial", size=12)
    for line in report_text.split(''):
        pdf.cell(0, 10, txt=line.strip(), ln=True)
    filename = f"hamal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return f"הדוח נשמר בשם: {filename}"