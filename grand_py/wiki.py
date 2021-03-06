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
        self.title = None
        self.pageid = None
        self.lat = None
        self.long = None
        self.response = None
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
        request = requests.get(url=self.api_url, params=self.parameters)
        if request.json()['query']['searchinfo']['totalhits'] != 0:
            self.response = request
            return True

    def clean_result(self, text):
        """Clean the summary from a type of content"""
        new_text = re.sub('\[(.*?)\]', '', text)
        new_text = re.sub('\((.*?)\)', '', new_text)
        new_text = re.sub('\/(.*?)\/', '', new_text)
        return new_text

    def get_data(self):
        """Get article data from a title"""
        self.title = self.response.json()['query']['search'][0]['title']
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
        if not self.clean_result(self.data['query']['pages'][self.pageid]['extract']) and \
                self.count <= 2:
            self.count += 1
            self.get_next_data()


    def get_next_title(self):
        """Select the next title in the dysambiguous page"""
        title = self.title
        while title == self.data['query']['search'][self.secondcount]['title']:
            self.secondcount += 1
            self.title = self.data['query']['search'][self.secondcount]['title']


    def get_next_data(self):
        """Reload a new data from a new title"""
        parameters = {"action"  : "query",
                      "format"  : "json",
                      "srsearch": self.search,
                      "list"    : "search"}
        self.data = requests.get(url=self.api_url, params=parameters).json()
        self.get_next_title()
        self.get_data()
