import requests


class Map:

    def __init__(self, address, place):
        self.api_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        self.search = address
        self.place = place
        self.parameters = {
            'address': self.search,
            'key'    : 'AIzaSyBlM1lBFayUTLiN8ZiwczP6DWfWGNNYlT8'
        }
        self.response = requests.get(url=self.api_url, params=self.parameters).json()
        self.data = None
        self.location = None
        self.latitude = None
        self.longitude = None

    def adress_exist(self):
        if not self.response['results']:
            return False
        else:
            self.location = self.response['results'][0]['geometry']['location']
            self.latitude = self.location['lat']
            self.longitude = self.location['lng']
            return True

    def location_exist(self):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        self.place += " france"
        parameters = {
            'input'    : self.place,
            'key'      : 'AIzaSyBlM1lBFayUTLiN8ZiwczP6DWfWGNNYlT8',
            'inputtype': 'textquery',
            'language' : 'fr',
            'fields'   : 'geometry/location'
        }
        self.response = requests.get(url=url, params=parameters).json()
        if self.response['results']:
            return True

