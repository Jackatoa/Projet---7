from grand_py.wiki import Wiki
import requests
import unittest


class WikiTests(unittest.TestCase):
    def test_wiki_clean_result(self):
        element = w.clean_result(
            "Nicolas Sarközy de Nagy-Bocsab, dit Nicolas Sarkozy (/ni.kɔ.la saʁ.kɔ.zi/c) ["
            "/ni.kɔ.la saʁ.kɔ.zi/c ]; ")
        assert element == "Nicolas Sarközy de Nagy-Bocsab, dit Nicolas Sarkozy  ; "


def test_wiki_exist(monkeypatch):
    class MockResponse:
        def json(self):
            return {'batchcomplete': '',
                    'continue': {'sroffset': 10, 'continue': '-||'},
                    'query'        : {'searchinfo': {'totalhits': 5481},
                                      'search'    : [{'ns'       : 0,
                                                      'title':'Test wiki',
                                                      'pageid'  : 675918,
                                                      'size': 281548,
                                                      'wordcount': 28186}]}
                    }

    def mock_get(url, params):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    assert w.exist() is True


def test_wiki_doesnt_exist(monkeypatch):
    class MockResponse:
        def json(self):
            return {'batchcomplete': '', 'continue': {'sroffset': 10, 'continue': '-||'},
                    'query'        : {'searchinfo': {'totalhits': 0},
                                      'search': [{'ns'       : 0,
                                                  'title'    :'Test wiki',
                                                  'pageid'   : 675918,
                                                  'size'     : 281548,
                                                  'wordcount': 28186}]}}

    def mock_get(url, params):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    assert w.exist() is None


w = Wiki("Openclassrooms France")
