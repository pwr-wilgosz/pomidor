from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

from popups import InfoPopup, ServReqPopup, EditTaskPopup, DeleteTaskPopup, AddListPopup
from listentry import ListEntry

from decorator import RawToGuiLists
#from kivy.core.window import Window
#Window.size = (480, 255)

Builder.load_file('./gui/main.kv')
# Builder.load_file('main.kv')

class PomidorApp(App):
    """ Main controller class
    """
    dataManip = None
    loginScr = None
    rootScr = None

    def __init__(self, manager, **kwargs):
        super(PomidorApp, self).__init__(**kwargs)
        self.dataManip = manager
        self.loginScr = LoginScr(manager, name='Login')
        self.rootScr = RootWidget(manager, name='Main app')

    def build(self):
        """ Launch GUI. Creates main widget - screen manager
        """
        root = ScreenManager()
        root.transition = SwapTransition()
        root.add_widget(self.loginScr)
        root.add_widget(self.rootScr)
        return root

    def RunServSync(self, auth_name, auth_pass):
        """ Launch service that covers serv sync operations, shows gui repr
        """
        print("i'm syncing with serv", auth_name, auth_pass)
        self.dataManip.ConnectAndSync(auth_name, auth_pass)

class LoginScr(Screen):
    """ View to ask for auth data (login/pass)
        STATUS: BASE: pass the view, perform sync on given data
    """
    dataManip = None
    login = None
    password = None

    def __init__(self, manager, **kwargs):
        super(LoginScr, self).__init__(**kwargs)
        self.dataManip = manager

    def LoginAction(self, login, password):
        """ Operation after submitting data for login
            login -
            pass -
        """
        print('Try to log in')
        self.login = login
        self.password = password

        logRes = self.dataManip.LoginToApp(login, password)
        if logRes == 'OK':
            self.show_login_ok()
            self.manager.current = self.manager.next()
        elif logRes == 'ServReq':
            self.show_serv_req()
        elif logRes == 'Fail':
            self.show_login_fail()

    def show_login_ok(self):
        loginOkText = 'Zalogowano!'
        p = InfoPopup(pop_descr=loginOkText)
        p.open()

    def show_serv_req(self):
        servReqText = 'Nie znaleziono danych uzytkownika w lokalnej bazie.\
                    Niezbedne jest polaczenie z serwerem w celu weryfikacji.'
        p = ServReqPopup(servReqText, self.login, self.password)
        p.open()

    def show_login_fail(self):
        loginFailText = 'Niepoprawne haslo.'
        p = InfoPopup(pop_descr=loginFailText)
        p.open()

class RootWidget(Screen):
    """ Main layout class. Ships all GUI widgets
    """
    lists_content=ObjectProperty(None)
    dataManip = None

    def __init__(self, manager, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.dataManip = manager
        self.lists_content.bind(minimum_height=self.lists_content.setter('height'))

    def on_enter(self):
        self.ReloadListsView()
        super(RootWidget, self).on_enter()

    def ReloadListsView(self):
        """ Prepares view to insert tasks and fetch tasks from db
        """
        print("Reloading lists view")
        self.lists_content.clear_widgets()
        rawLists = self.dataManip.GetListsToView()
        guiLists = RawToGuiLists(rawLists)
        for i in guiLists:
            self.lists_content.add_widget(i)

    def add_new_list(self, inputField):
        # info = "Adding new list: '{name}'".format(name=inputField.text)
        p = AddListPopup(inputField.text)
        p.open()


if '__main__' == __name__:
    PomidorApp().run()
