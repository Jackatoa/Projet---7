import requests
from grand_py.config import GOOGLE_API_KEY

class Map:
    """Contains all the google api"""
    def __init__(self, address, place):
        self.api_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        self.search = address
        self.place = place
        self.response = self.get_response(self.search)
        self.data = None
        self.location = None
        self.latitude = None
        self.longitude = None

    def get_response(self, search):
        parameters = {
            'address': search,
            'key'    : GOOGLE_API_KEY
        }
        return requests.get(url=self.api_url, params=parameters)

    def adress_exist(self):
        """Check if an adress can be found"""
        if not self.response.json()['results']:
            return False
        else:
            self.location = self.response.json()['results'][0]['geometry']['location']
            self.latitude = self.location['lat']
            self.longitude = self.location['lng']
            return True

    def location_exist(self, newarg):
        """Check if a location can be found"""
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        place = self.place + newarg
        parameters = {
            'input'    : place,
            'key'      : GOOGLE_API_KEY,
            'inputtype': 'textquery',
            'language' : 'fr',
            'fields'   : 'geometry/location'
        }
        self.response = requests.get(url=url, params=parameters)
        if self.response.json()['results']:
            return True
