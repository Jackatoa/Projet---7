import requests

class Wiki:

    def __init__(self, search):
        self.api_url = "https://fr.wikipedia.org/w/api.php"
        self.search = search
        self.parameters = {"action": "query", "format": "json", "srsearch": self.search,
                           "list": "search"}
        self.response = requests.get(self.api_url, params=self.parameters)
        self.data = self.response.json()
        self.title = self.data['query']['search'][0]['title']


    def getSummary(self):
        print(self.data['query']['search'][0]['title'])
        parameters = {"action": "query", "prop": "extracts", "format": "json", "titles":
            self.title, "exintro": "1", "explaintext": "1"}
        new_resp = requests.get(self.api_url, params=parameters)
        print(new_resp.json())
        print(next(iter(new_resp.json()['query']['pages'])))
        pageid= next(iter(new_resp.json()['query']['pages']))
        print(new_resp.json()['query']['pages'][pageid]['extract'])
        return new_resp.json()['query']['pages'][pageid]['extract']

    def is_location(self):
        return False

    def exist(self):
        if self.response.status_code == 200:
            return True


