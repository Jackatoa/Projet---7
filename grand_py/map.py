import requests


class Map:

    def __init__(self, search):
        self.api_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        self.search = search
        self.parameters = {
            'address': self.search,
            'key': ''
        }
        self.response = requests.get(url=self.api_url, params=self.parameters).json()
        self.location = None
        self.latitude = None
        self.longitude = None

    def exist(self):
        if not self.response['results']:
            return False
        else:
            self.location = self.response['results'][0]['geometry']['location']
            self.latitude = self.location['lat']
            self.longitude = self.location['lng']
            return True









