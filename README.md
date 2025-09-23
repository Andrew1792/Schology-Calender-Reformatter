# Schology-Calender-Reformatter

A simple Python script to convert a `.ics` calendar file downloaded from Schoology into a clean format that imports correctly into Google Calendar as all-day events.

## The Problem

When you export your calendar from Schoology, assignments are often created as events due at 11:59 PM. When importing this file into Google Calendar, these can show up as awkwardly timed events, create timezone issues, or fail to appear as clean "all-day" events.

## The Solution

This script reads your original `schoology.ics` file, extracts the essential information for each event (like the assignment title and due date), and builds a brand new, clean `.ics` file from scratch. Each event is created using the official iCalendar standard for all-day events, which ensures maximum compatibility with Google Calendar and other services.

This "rebuild" approach avoids issues with hidden properties, timezone conflicts, or non-standard formatting that may exist in the original file.

## Requirements

* Python 3.6+
* The `icalendar` library

## Installation

1.  Clone this repository or download the files.
2.  Install the required dependency using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Download your calendar** from Schoology.
2.  **Rename the file** to `schoology.ics` and place it in the same folder as the `format_ics.py` script.
3.  **Run the script** from your terminal:
    ```bash
    python format_ics.py
    ```
4.  A new file named `google_calendar_formatted.ics` will be created.
5.  **Import this new file** into your Google Calendar. All your assignments will now appear as proper all-day events on their due dates.

## License

This project is licensed under the MIT License.