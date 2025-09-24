import uuid
from icalendar import Calendar, Event
from datetime import datetime, timedelta

def convert_schoology_ics(input_filename, output_filename):
    """
    Reads a Schoology ICS file and creates a new, clean calendar with all 
    assignments converted to proper all-day events on the correct local due date.
    """
    try:
        local_tz = datetime.now().astimezone().tzinfo
        print(f"Detected local timezone: {local_tz}")

        with open(input_filename, 'rb') as f:
            old_cal = Calendar.from_ical(f.read())
        
        new_cal = Calendar()
        new_cal.add('prodid', '-//Schoology All-Day Converter//')
        new_cal.add('version', '2.0')

        converted_count = 0
        
        for component in old_cal.walk('VEVENT'):
            summary = component.get('summary')
            description = component.get('description', '')
            
            # Take the original datetime (UTC) and make the date match up with your timezone
            utc_dt = component.get('dtstart').dt
            local_dt = utc_dt.astimezone(local_tz)
            correct_local_date = local_dt.date()

            new_event = Event()
            new_event.add('summary', summary)
            new_event.add('description', description)
            
            # Create the all-day event on the correct local date.
            new_event.add('dtstart', correct_local_date)
            new_event.add('dtend', correct_local_date + timedelta(days=1))
            
            new_event.add('dtstamp', datetime.now())
            new_event.add('uid', f"{uuid.uuid4()}@google.com")

            new_cal.add_component(new_event)
            converted_count += 1
            
        with open(output_filename, 'wb') as f:
            f.write(new_cal.to_ical())
            
        print(f"\n✅ Success! Rebuilt {converted_count} events on the correct local due date.")
        print(f"Your new calendar file is ready: '{output_filename}'")

    except FileNotFoundError:
        print(f"❌ Error: The file '{input_filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main execution ---
if __name__ == "__main__":
    input_file = "calendar.ics"
    output_file = "google_calendar_formatted.ics"
    
    convert_schoology_ics(input_file, output_file)