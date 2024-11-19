import json

from scraper import ScrapeLaunches as sl
import datetime

def sort_net_confirmed(launches):
    sorted_launches = {"Confirmed": [], "NET": []}
    for launch in launches:
        date_first_three_chars = launch["Date"][0:3]
        if date_first_three_chars == "NET":
            sorted_launches["NET"].append(launch)
        else:
            sorted_launches["Confirmed"].append(launch)
    return sorted_launches

def __get_timezone_offset():
    timezone_info = datetime.datetime.now().astimezone().tzinfo
    timezone_offset = str(datetime.datetime.now(tz=timezone_info))[-6:-3]
    timezone_offset_value = timezone_offset[1:].lstrip("0")
    if timezone_offset == "+00": timezone_offset_value = timezone_offset[1:]
    timezone_offset = timezone_offset[0] + timezone_offset_value
    return timezone_offset

def __extract_date_and_time(string):
    date_time_string = string["Date"]
    date = datetime.datetime.strptime(date_time_string[0:17].strip(), "%a %b %d, %Y").date()
    time = date_time_string[-9:].split(" ")[0].split(":")

    return date, time

def convert_timezone(dated_launches:list) -> list:
    timezone_offset = __get_timezone_offset()
    converted_launches = []
    for launch in dated_launches:
        #Get date and time (unconverted) from the launch item
        launch_date, launch_time = __extract_date_and_time(launch)
        #Convert the hour to the local timezone
        if timezone_offset == "+": timezone_offset = "+1"
        converted_hour = eval(launch_time[0].lstrip("0") + timezone_offset)

        #If converted time rolls over a day
        if converted_hour >= 24:
            if int(timezone_offset) > 0: day_offset = 1 #Day ahead
            else: day_offset = -1 #Day behind
            converted_hour -= 24
            launch_date = datetime.timedelta(days=day_offset) + launch_date #Adding day to date

        launch_time[0] = str(converted_hour).zfill(2) #Padding trailing 0's where necessary to make correct time format

        launch_date = launch_date.strftime("%a %b %d, %Y")

        converted_launches.append(launch.copy()) #Must be COPY otherwise will alter parsed attribute and mess stuff up
        converted_launches[-1]["Date"] = f"{launch_date} {launch_time[0]}:{launch_time[1]}"

    return converted_launches

if __name__ == "__main__":
    ...