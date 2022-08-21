# WSO_ical

### Description
This is a simple program i wrote to help me with my current part-time job scheduling.
The program extracts important metadata from the webpage of the Vienna State Opera and transfroms it into .ics files to get imported into Google Calendar.
The UI is console based.
It's simple to operate:
1) You will be prompted to enter a month (case insensitive)
2) You will be prompted to enter the dates on which you don't work
3) All working dates will be exported in a folder in the format *date_name.ics*

Afterwards files can be manually imported to Google Calendar

### Used Libraries
- Beautiful Soup/BS4
- icalendar

### Final Thoughts
- This project has taught me about webscraping and reading (meta)data from static webpages.
- A thing that could be improved is to connect to the Google Calendar API and automatically import the work dates in the calendar.
- The UI can definitely be changed (as there is currently no UI).
- This project is bound to break. Rather than look for hidden APIs or DB connections, I've based it on extracting data from the webpage, which makes it easely breakable if the structure is changed. 
