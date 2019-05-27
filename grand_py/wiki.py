import requests
import re
class Wiki:
    """Contains all the wiki api"""
    def __init__(self, search):
        self.api_url = "https://fr.wikipedia.org/w/api.php"
        self.search = search
        self.parameters = {"action": "query",
                           "format": "json",
                           "srsearch": self.search,
                           "list": "search"}
        self.response = requests.get(url=self.api_url, params=self.parameters)
        self.title = None
        self.pageid = None
        self.lat = None
        self.long = None
        self.data = None

    def getSummary(self):
        """Return the wikipedia summary"""
        return self.clean_result(self.data['query']['pages'][self.pageid]['extract'])

    def is_location(self):
        """Check if this place got coordinates on the wiki"""
        parameters = {
            'action': "query",
            'prop': "coordinates",
            'titles': self.title,
            'format': "json"
        }
        new_resp = requests.get(url=self.api_url, params=parameters)
        self.pageid = next(iter(new_resp.json()['query']['pages']))
        print("islocation  new_resp.json() = {0}".format(new_resp.json()))
        data = new_resp.json()
        if 'coordinates' in data['query']['pages'][self.pageid].keys():
            print("wiki is location check")
            self.lat = new_resp.json()['query']['pages'][self.pageid]['coordinates'][0]['lat']
            self.long = new_resp.json()['query']['pages'][self.pageid]['coordinates'][0]['lon']
            return True

    def exist(self):
        """Check if something can be found with the user input"""
        print("self.data = {0}".format(self.response.json()))
        if self.response.json()['query']['searchinfo']['totalhits'] != 0:
            self.title = self.response.json()['query']['search'][0]['title']
            print(self.title)
            self.get_data()
            return True

    def clean_result(self, text):
        """Clean the summary from a type of content"""
        new_text = re.sub('\[(.*?)\]', '', text)
        new_text = re.sub('\((.*?)\)', '', new_text)
        return new_text

    def get_data(self):
        parameters = {"action"     : "query",
                      "prop"       : "extracts",
                      "format"     : "json",
                      "titles"     : self.title,
                      "exintro"    : "1",
                      "explaintext": "1",
                      "exsentences": "2"
                      }
        self.data = requests.get(url=self.api_url, params=parameters).json()
        self.pageid = next(iter(self.data['query']['pages']))
        print("extract {0}".format(self.clean_result(self.data['query']['pages'][self.pageid]['extract'])))
        if not self.clean_result(self.data['query']['pages'][self.pageid]['extract']):
            parameters = {"action": "query",
                           "format": "json",
                           "srsearch": self.title,
                           "list": "search"}
            self.data = requests.get(url=self.api_url, params=parameters).json()
            self.title = self.data['query']['search'][0]['title']
            self.get_data()



