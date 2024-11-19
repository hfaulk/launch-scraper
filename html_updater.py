from scraper import ScrapeLaunches as sl
from launch_processor import sort_net_confirmed, convert_timezone

a = sl(5)
launches = a.get_launches()

net_and_confirmed = sort_net_confirmed(launches)

confirmed_tz = convert_timezone(net_and_confirmed["Confirmed"])

net_and_confirmed["Confirmed"] = confirmed_tz

with open("index.html", "r", encoding="UTF-8") as f:
    contents = f.readlines()
    html_content = [i.strip() for i in contents]

for line in html_content:
    if "<p>" in line:
        line_index = html_content.index(line)
        
new_content = ""

for launch in net_and_confirmed["Confirmed"]:
    new_content += f"<p>{launch["Date"]} / {launch["Vehicle"]} / {launch["Mission"]} / {launch["Agency"]} / {launch["Location"]}</p>"
for launch in net_and_confirmed["NET"]:
    new_content += f"<p>{launch["Date"]} / {launch["Vehicle"]} / {launch["Mission"]} / {launch["Agency"]} / {launch["Location"]}</p>"

html_content[line_index] = new_content

with open("index.html", "w", encoding="UTF-8") as f:
    f.write("\n".join(html_content))