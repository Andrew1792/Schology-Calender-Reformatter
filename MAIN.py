from icalendar import Calendar
from datetime import datetime, timedelta

def convert_schoology_ics(input_filename, output_filename):
    """
    Reads a Schoology ICS file, converts events due at 11:59 PM to all-day events,
    and saves the result to a new file. This version is more robust and also
    removes the DURATION property.
    """
    try:
        with open(input_filename, 'rb') as f:
            old_cal = Calendar.from_ical(f.read())
        
        new_cal = Calendar()

        for key, value in old_cal.items():
            new_cal.add(key, value)

        converted_count = 0

        for component in old_cal.walk('VEVENT'):
            dtstart = component.get('dtstart').dt

            if isinstance(dtstart, datetime) and dtstart.hour == 23 and dtstart.minute == 59:
                event_date = dtstart.date()
                
                # --- THIS IS THE KEY FIX ---
                # To create a true all-day event, we must remove all properties
                # that define a specific time or duration.
                if 'dtend' in component:
                    del component['dtend']
                if 'duration' in component:
                    del component['duration']  # <-- The new, important line!
                
                # Now we set the correct all-day properties.
                component['dtstart'].dt = event_date
                component.add('dtend', event_date + timedelta(days=1))
                
                converted_count += 1

            new_cal.add_component(component)

        with open(output_filename, 'wb') as f:
            f.write(new_cal.to_ical())
            
        print(f"✅ Success! Converted {converted_count} events to all-day events.")
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