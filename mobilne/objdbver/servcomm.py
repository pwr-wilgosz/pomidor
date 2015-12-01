import json
import urllib
from kivy.network.urlrequest import UrlRequest

class ServComm():
    server_url = None
    authKey = ''

    def __init__(self, servUrl, loginDataPair = None):
        self.server_url = servUrl
        if loginDataPair != None:
            self.authKey = self.login(loginDataPair)

    def login(self, loginDataPair):
        """Logowanie do systemu, utworzenie sesji, pobranie identyfikatora
            loginDataPair - login [0] i haslo [1] dostepowe do serwera
        returns: ciag do autoryzacji (klucz sesji)
        """
        server_url = self.server_url
        login = loginDataPair[0]
        password = loginDataPair[1]
        #wyslanie danych logowania
        res = self.post(server_url + "/login.json", params=[
                ['email', login], ['password', password]],
                description="Inicjalizacja sesji")
        bodyDict = json.loads(res.body)
        return bodyDict['access_token']

    def processWholeData(self):
        """Pobranie danych list zadaniowych w celu wykonywania szczegolowych zapytan
        returns: dane list zadaniowych
        """
        getListsUrl = "{serv_url}/{task}?access_token={token}".\
                        format(serv_url=self.server_url, task="lists",
                        token=self.authKey)

        #Zapytanie o listy
        res = self.get(getListsUrl, description='Pobieranie list zadan')
        body = json.loads(res.body)

        #Sprawdzenie poprawnosci odpowiedzi
        self.assertEqual(res.code, 200)
        self.assertEqual(body['lists_count'], len(body['lists']))

        return body['lists']

    def getListsData(self):
        """Pobranie danych list zadaniowych w celu wykonywania szczegolowych zapytan
        returns: dane list zadaniowych
        """
        getListsUrl = "{serv_url}/{task}?access_token={token}".\
                        format(serv_url=self.server_url, task="lists",
                        token=self.authKey)

        #Zapytanie o listy
        res = self.get(getListsUrl, description='Pobieranie list zadan')
        body = json.loads(res.body)

        #Sprawdzenie poprawnosci odpowiedzi
        self.assertEqual(res.code, 200)
        self.assertEqual(body['lists_count'], len(body['lists']))

        return body['lists']

    def getListsRetRandom(self):
        """Pobiera listy zadaniowe, zwraca jedna (losowa) z nich
        returns: dane losowej listy
        """
        lists = self.getListsData()
        listsCount = len(lists)
        randId = random.randint(0, listsCount)
        return lists[randId]

    def getTasksFromListsWhere(self,lists, givenId = 0):
        """Pobiera zadania nalezace do podanych list
            lists - slownik wszystkich list ('lists')
            givenId - id konkretnej listy; jesli nie podano - uwzglednia wszystkie
        returns: slownik list(y) uzupelniony o zadania
        """
        tasks = []

        if givenId != 0:
            listsIdToFetch.append(givenId)
        else:
            for it in listsDetails:
                 tasks = self.getTasksFromList(it['id'])
                 it['tasks'] = tasks


        # for listId in listsIdToFetch:

    def getTasksFromList(self, listId):
        """Pobiera zadania nalezace do danej listy
            listId - id listy do pobrania
        returns: lista slownikow opisujacych zadania
        """
        getFunctionUrl = "{serv_url}/lists/{lId}/tasks?access_token={token}".\
                            format(serv_url=self.server_url, lId=listId,
                            token=self.authKey)
        res = self.get(getListsUrl, description='Pobieranie zadan z listy')
        body = json.loads(res.body)
        return body['tasks']
