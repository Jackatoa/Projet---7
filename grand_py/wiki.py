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
        self.data = self.response.json()
        self.title = None
        self.pageid = None
        self.lat = None
        self.long = None

    def getSummary(self):
        """Return the wikipedia summary"""
        self.get_title()
        parameters = {"action": "query",
                      "prop": "extracts",
                      "format": "json",
                      "titles": self.title,
                      "exintro": "1",
                      "explaintext": "1",
                      "exsentences": "2"
                      }
        new_resp = requests.get(url=self.api_url, params=parameters)
        self.pageid = next(iter(new_resp.json()['query']['pages']))
        return self.clean_result(new_resp.json()['query']['pages'][self.pageid]['extract'])

    def is_location(self):
        """Check if this place got coordinates on the wiki"""
        self.get_title()
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
        if self.data['query']['searchinfo']['totalhits'] != 0:
            return True

    def clean_result(self, text):
        """Clean the summary from a type of content"""
        new_text = re.sub('\[(.*?)\]', '', text)
        new_text = re.sub('\((.*?)\)', '', new_text)
        return new_text

    def get_title(self):
        """Return the title of a page"""
        self.title = self.data['query']['search'][0]['title']

