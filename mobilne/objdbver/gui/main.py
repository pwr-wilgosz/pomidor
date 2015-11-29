# -*- coding: utf-8 -*-
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder

from popups import InfoPopup, ServReqPopup, EditTaskPopup, DeleteTaskPopup, AddListPopup
from listentry import ListEntry

from decorator import RawToGuiLists, RawToGuiTasks
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
    changeLables = None

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

    def ListTaskPickAction(self, list_id = None, task_id = None):
        """ Store user pick decision, ask for update GUI pick repr
            list_id - new user list choise (not required)
            task_id - new user task choise (not required)
        returns: None
        """
        if task_id != None:
            self.dataManip.SetTask(task_id)
        else:
            self.dataManip.SetList(list_id)

        listTaskNamePair = self.dataManip.PickedListTaskNamePair()
        self.rootScr.SetPagesLabels(listTaskNamePair[0], listTaskNamePair[1])
        self.rootScr.ReloadTasksView()



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
    lists_content = ObjectProperty(None)
    task_imp_urg = ObjectProperty(None)
    task_nimp_urg = ObjectProperty(None)
    task_imp_nurg = ObjectProperty(None)
    task_nimp_nurg = ObjectProperty(None)
    list_label = StringProperty('Wybierz liste')
    task_label = StringProperty('Wybierz zadanie')
    dataManip = None

    def __init__(self, manager, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.dataManip = manager
        self.lists_content.bind(minimum_height=self.lists_content.setter('height'))

    def on_enter(self):
        app = App.get_running_app()
        app.ListTaskPickAction()
        self.ReloadListsView()
        super(RootWidget, self).on_enter()

    def ReloadListsView(self):
        """ Prepares view to insert listsGuiObj and fetch lists from db
        """
        print("Reloading lists view")
        self.lists_content.clear_widgets()
        rawLists = self.dataManip.GetListsToView()
        guiLists = RawToGuiLists(rawLists)
        for i in guiLists:
            self.lists_content.add_widget(i)

    def ReloadTasksView(self):
        """ Prepares view to insert tasksGuiObj and fetch tasks from db.
            Called after task pick action
        """
        print("Reloading tasks view")
        self.ClearTaskGrid()
        rawTasks = self.dataManip.GetTasksToView()
        guiTasks = RawToGuiTasks(rawTasks)
        self.AddTasksToGrid(guiTasks)

    def ClearTaskGrid(self):
        self.task_imp_urg.clear_widgets()
        self.task_nimp_urg.clear_widgets()
        self.task_imp_nurg.clear_widgets()
        self.task_nimp_nurg.clear_widgets()

    def AddTasksToGrid(self, guiTasks):
        prior = 0
        for i in guiTasks:
            prior = i.priority
            if prior == 1:
                self.task_imp_urg.add_widget(i)
            elif prior == 2:
                self.task_nimp_urg.add_widget(i)
            elif prior == 3:
                self.task_imp_nurg.add_widget(i)
            else:
                self.task_nimp_nurg.add_widget(i)

    def SetPagesLabels(self, list_name, task_name):
        """ Updates pages labels after user pick (action call)
        """
        print("Change-label call!")
        list_label = 'Wybór listy'
        task_label = '[color=#222]Wybór zadania[/color]'
        if list_name != None:
            list_label += ' | [b]{list}[/b]'.format(list = list_name)
            if task_name != None:
                task_label += '[color=#222] | [b] {list}[/b] - [i]{task}[/i][/color]'.\
                        format(list = list_name, task = task_name)

        self.list_label = list_label
        self.task_label = task_label

    def add_new_list(self, inputField):
        # info = "Adding new list: '{name}'".format(name=inputField.text)
        p = AddListPopup(inputField.text)
        p.open()


if '__main__' == __name__:
    PomidorApp().run()
