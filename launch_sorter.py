from scraper import ScrapeLaunches


class Sorter:
    def __init__(self, all_launches:dict):
        sort_types = [["date"], ["agency"], [""]]
        if type(all_launches) == list:
            self.launches = all_launches
        else:
            self.launches = all_launches["Confirmed"] + all_launches["NET"]

class Filterer:
    ...

if __name__ == "__main__":
    import scraper as sc
    import launch_processor as lp

    scraper = sc.ScrapeLaunches()
    launches = scraper.get_launches()

    net_and_confirmed_launches = lp.sort_net_confirmed(launches)

    local_timezone_launches = lp.convert_timezone(net_and_confirmed_launches["Confirmed"])

    net_and_confirmed_launches["Confirmed"] = local_timezone_launches

    sorter = Sorter(net_and_confirmed_launches)