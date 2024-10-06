import requests
from bs4 import BeautifulSoup

class ScrapeLaunches:
    """
    A class that scrapes "https://nextspaceflight.com/launches/" for all current scheduled rocket launches.
    ONLY METHOD THAT NEEDS TO BE CALLED IS get_launches(). EVERYTHING ELSE HAPPENS UPON INSTANTIATION.

    Methods
    ------
        __parse_html():
            Gets the raw specific information from the received html code.
        __parse_data():
            Iterates over all the parsed html data and processes it into a list of dictionaries.
        get_launches():
            Returns the list produced by __parse_data().
    """
    def __init__(self, number_of_pages: int = 1):
        """
        Checks connection to the url, then processes all the required data using the other methods.

        Attributes
        --------
            number_of_pages: int
                Number of pages scraper will retrieve html for (more pages = more launches). 1 by default.

        See Also
        --------
        __parse_html()
        __parse_data()
        """
        all_html_content = []

        for page in range(1, number_of_pages + 1):
            self.url = f"https://nextspaceflight.com/launches/?page={page}"
            response = requests.get(self.url)

            if response.status_code == 200:
                all_html_content.append(response.text)
            else:
                raise Exception(f"Data Retrieval Failed. Error Code: {response.status_code}")

        self.html_content = "".join(all_html_content)

        self.__parse_html()
        self.__parse_data()

    def __parse_html(self):
        """
        Gets the raw specific information from the received html code.

        See Also
        --------
        __init__()
        __parse_html()
        __parse_data()
        """
        soup = BeautifulSoup(self.html_content, 'html.parser')

        self.launch = soup.find_all("h5")
        self.launch_info = soup.find_all("div", class_="mdl-card__supporting-text")
        self.agency_info = soup.find_all("div", class_="mdl-card__title-text")

        del self.agency_info[::2]

    def __parse_data(self):
        """
        Iterates over all the parsed html data and processes it into a list of dictionaries.

        See Also
        --------
        __init__()
        __parse_html()
        __parse_data()
        """
        self.launches = []

        for index, launch in enumerate(self.launch):
            # Getting vehicle & mission
            vehicle = launch.text.strip().split("|")[0].strip()
            mission = launch.text.strip().split("|")[1].strip()
            agency = self.agency_info[index].text.strip()

            # Separating date/time and location
            info = self.launch_info[index].text.splitlines()
            all_info = []
            for info in info:
                if info.count(" ") == len(info):
                    pass
                else:
                    all_info.append(info.strip())

            # Combining all launch info
            launch = {"Vehicle": vehicle, "Mission": mission, "Agency": agency, "Date": all_info[0],
                      "Location": all_info[1]}
            self.launches.append(launch)

    def get_launches(self):
        """
        Returns the list produced by __parse_data().

        Returns
        -------
        List

        See Also
        --------
        __parse_html()
        __parse_data()
        """
        return self.launches

if __name__ == "__main__":
    scraper = ScrapeLaunches()
    launches = scraper.get_launches()

    for i in launches:
        print(i["Vehicle"], i["Mission"], i["Agency"], i["Date"])