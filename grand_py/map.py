import requests


class Map:
    """Contains all the google api"""
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
        """Check if an adress can be found"""
        if not self.response['results']:
            return False
        else:
            self.location = self.response['results'][0]['geometry']['location']
            self.latitude = self.location['lat']
            self.longitude = self.location['lng']
            return True

    def location_exist(self, newarg):
        """Check if a location can be found"""
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        place = self.place + newarg
        parameters = {
            'input'    : place,
            'key'      : 'AIzaSyBlM1lBFayUTLiN8ZiwczP6DWfWGNNYlT8',
            'inputtype': 'textquery',
            'language' : 'fr',
            'fields'   : 'geometry/location'
        }
        self.response = requests.get(url=url, params=parameters).json()
        if self.response['results']:
            return True


    def map_exist(self):
        if self.location_exist(" France"):
            print("place france exist")
            return True
        elif self.location_exist(" commune"):
            print("place commune exist")
            return True
        elif self.adress_exist():
            print("adress exist")
            return True
