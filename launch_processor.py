from scraper import ScrapeLaunches as sl

#Scrape all current scheduled launches
scraper = sl(2)
all_launches = scraper.get_launches()

def sort_net_confirmed(launches):
    sorted_launches = {"Confirmed": [], "NET": []}
    for launch in launches:
        date_first_three_chars = launch["Date"][0:3]
        if date_first_three_chars == "NET":
            sorted_launches["NET"].append(launch)
        else:
            sorted_launches["Confirmed"].append(launch)
    return sorted_launches

if __name__ == "__main__":
    sorted = sort_net_confirmed(all_launches)
    for i in sorted["NET"]:
        print(f"{i["Agency"]}, {i["Mission"]}, {i["Vehicle"]}, {i["Date"]}, {i["Location"]}")