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
        self.count = 0
        self.secondcount = 0

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
        data = new_resp.json()
        if 'coordinates' in data['query']['pages'][self.pageid].keys():
            self.lat = new_resp.json()['query']['pages'][self.pageid]['coordinates'][0]['lat']
            self.long = new_resp.json()['query']['pages'][self.pageid]['coordinates'][0]['lon']
            return True

    def exist(self):
        """Check if something can be found with the user input"""
        if self.response.json()['query']['searchinfo']['totalhits'] != 0:
            self.title = self.response.json()['query']['search'][0]['title']
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
        print("get data title {0}".format(self.title))
        self.data = requests.get(url=self.api_url, params=parameters).json()
        print("self.data 1 {0}".format(self.data))
        self.pageid = next(iter(self.data['query']['pages']))
        if not self.clean_result(self.data['query']['pages'][self.pageid]['extract']) and \
                self.count <= 2:
            self.count += 1
            parameters = {"action": "query",
                           "format": "json",
                           "srsearch": self.search,
                           "list": "search"}
            self.data = requests.get(url=self.api_url, params=parameters).json()
            print("data count{0}".format(self.data))
            self.get_new_title()
            self.get_data()

    def get_new_title(self):
        title = self.title
        print("title avant new {0}".format(title))
        while title == self.data['query']['search'][self.secondcount]['title']:
            print(self.data['query']['search'][self.secondcount]['title'])
            self.secondcount += 1
            self.title = self.data['query']['search'][self.secondcount]['title']
            print(self.title)
