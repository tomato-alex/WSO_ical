from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, vCalAddress, vText
import os
from pathlib import Path


class OperaEvent:
    # constructor
    def __init__(self, name, start, end, date):
        self.name = name
        self.start = start
        self.end = end
        self.date = date

    # getters
    def getName(self):
        return self.name

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getDate(self):
        return self.date


def transform_date(_input):
    # this function takes a text format input and transforms it into a WSO link date
    # if the input is not a month, it returns nothing
    # the type of date is YYYY-MM-DD where date is always 01 and YYYY is determined by the month
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    input_t = _input.lower()
    num_month = 1
    for month in months:
        if input_t == month:
            break
        else:
            num_month += 1
    if num_month > 12:
        return "Wrong input"

    curr_month = datetime.today().month
    curr_year = datetime.today().year
    # ternary way to transform the selected month into a WSO link date
    check_date = (
        str(curr_year if curr_month <= num_month else curr_year + 1)
        + "-"
        + (str(num_month) if num_month >= 10 else "0" + str(num_month))
        + "-01/"
    )
    return check_date


def fetch_perf(_link):
    # this function fetches the webpage from the _link
    # it then identifies all of the events
    # and formats their metadata to datetime format
    # to_do: it also saves and should return a list of the events
    # the following lines return a page from the month of the WSO website
    # then we fetch the list of events from the site
    # class is div class, needs to be clarified with "_" because class is a python keyword
    # the end line makes an array with each item from the calendar-list-item class
    # which specifies a certain event
    page = requests.get(_link)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="calendar-list load-culturall")
    event_elements = results.find_all("div", class_="calendar-list-item")

    # the following code formats the event_elements, picking only the metadata
    # each event might contain more than one actual performance
    # so for each metaData class in the calendar-list-item item we separate them
    # then comparing to certain keywords for events we dont participate in
    # after which we single out the name, start and end
    # and create a new Event class entity
    # it is possible to also extract the adress and more data from the metadata class
    events = []  # array of Event class types to be returned
    for event in event_elements:
        metaData = event.find_all("div", class_="metadata")
        # metaData is an array (even if we have a single event in the day)
        for data in metaData:
            name = data.find("span", itemprop="name")
            if (
                "Open" in name.text
                or "Keine Vorstellung" in name.text
                or "Abgesagt" in name.text
                or "Ensemblematinee" in name.text
            ):
                continue
            start_h = data.find("span", itemprop="startDate")
            end_h = data.find("span", itemprop="endDate")
            date_format = "%Y%m%d"
            # format time and date to datetime format
            start_time = datetime.fromisoformat(start_h.text) - timedelta(
                hours=1.5
            )  # .strftime(date_format)
            end_time = datetime.fromisoformat(end_h.text)  # .strftime(date_format)
            date = datetime.fromisoformat(start_h.text).strftime(date_format)
            events.append(OperaEvent(name.text, start_time, end_time, date))

    return events


def create_event(event_):
    cal = Calendar()
    cal.add("attendee", "MAILTO:xxx@gmail.com")

    event = Event()
    event.add("summary", "Work")
    event.add("dtstart", event_.getStart())
    event.add("dtend", event_.getEnd())
    cal.add_component(event)

    directory = str(Path(__file__).parent.parent) + "/ical/"
    # print("ics file will be generated at ", directory)
    f = open(
        os.path.join(
            directory,
            event_.getDate()
            + "_"
            + event_.getName()
            .replace(" ", "_")
            .replace(",", "_")
            .replace("<br>", "_")
            .replace(".", "_")
            + ".ics",
        ),
        "wb",
    )
    f.write(cal.to_ical())
    f.close()


if __name__ == "__main__":
    link = "https://www.wiener-staatsoper.at/spielplan-kartenkauf/liste/refDate/"
    monthInput = input("Select a month: ")
    monthInput = transform_date(monthInput)
    print(link + monthInput)
    freeDays = []
    while 1:
        freeDays.append(input("When are you having free?(0 to break): "))
        if freeDays[-1] == "0":
            freeDays.pop()
            break
        if int(freeDays[-1]) < 10:
            freeDays[-1] = "0" + freeDays[-1]
    # print(freeDays)
    events_list = fetch_perf(link + monthInput)
    for event in events_list:
        print(event.getName(), event.getStart(), event.getEnd())
        # print(event.getStart().strftime("%d"))
        if not event.getStart().strftime("%d") in freeDays:
            create_event(event)

    # print(event_elements[0])
