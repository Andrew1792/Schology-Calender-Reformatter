import uuid
from icalendar import Calendar, Event
from datetime import datetime, timedelta

def convert_schoology_ics(input_filename, output_filename):
    """
    Reads a Schoology ICS file and creates a new, clean calendar with all 
    assignments converted to proper all-day events on their due date.
    This is a robust method that builds events from scratch to avoid errors.
    """
    try:
        with open(input_filename, 'rb') as f:
            old_cal = Calendar.from_ical(f.read())
        
        # 1. Create a completely new, clean calendar object
        new_cal = Calendar()
        new_cal.add('prodid', '-//Schoology All-Day Converter//')
        new_cal.add('version', '2.0')

        converted_count = 0
        
        # 2. Loop through every event from the original file
        for component in old_cal.walk('VEVENT'):
            summary = component.get('SUMMARY')
            description = component.get('DESCRIPTION', '')
            dtstart = component.get('dtstart').dt

            # We get the correct date regardless of the original time.
            if isinstance(dtstart, datetime):
                event_date = dtstart.date()
            else: # If it's already a date object
                event_date = dtstart

            # 3. Create a brand new, clean event from scratch
            new_event = Event()
            new_event.add('summary', summary)
            new_event.add('description', description)

            # 4. Set the ONLY date/time properties to be all-day.
            new_event.add('dtstart', event_date - timedelta(days=1))
            new_event.add('dtend', event_date)
            
            # 5. Add essential properties for compatibility
            new_event.add('dtstamp', datetime.now()) # Timestamp for when it was created
            new_event.add('uid', f"{uuid.uuid4()}@google.com") # A unique ID for the event

            # 6. Add the brand new, clean event to our new calendar
            new_cal.add_component(new_event)
            converted_count += 1
            
        # 7. Write the new calendar to the output file
        with open(output_filename, 'wb') as f:
            f.write(new_cal.to_ical())
            
        print(f"✅ Success! Rebuilt {converted_count} events as clean, all-day events.")
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