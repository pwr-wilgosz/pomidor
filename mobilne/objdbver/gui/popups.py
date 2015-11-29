from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.app import App

class InfoPopup(Popup):
    pop_descr = StringProperty()

    def __init__(self, pop_descr, **kwargs):
        self.pop_descr = pop_descr
        super(InfoPopup, self).__init__(**kwargs)

    def AcceptAction(self):
        self.dismiss()

class AddListPopup(InfoPopup):
    name = ''

    def __init__(self, new_name, **kwargs):
        infoText = 'Lista "{l}" zostala pomyslnie zapisana.'.format(l=new_name)
        self.name = new_name
        super(AddListPopup, self).__init__(infoText, **kwargs)

    def AcceptAction(self):
        self.PerformAction()
        self.CloseAndReload()

    def PerformAction(self):
        App.get_running_app().dataManip.SubmitList(self.name)

    def CloseAndReload(self):
        App.get_running_app().rootScr.ReloadListsView()
        self.dismiss()

class ServReqPopup(Popup):
    pop_descr = StringProperty()
    login = None
    password = None

    def __init__(self, pop_descr, login, password, **kwargs):
        super(ServReqPopup, self).__init__(**kwargs)
        self.pop_descr = pop_descr
        self.login = login
        self.password = password

class EditTaskPopup(Popup):
    list_id = ''
    listEntry = None

    def __init__(self, listEntry, **kwargs):
        super(EditTaskPopup, self).__init__(**kwargs)
        self.list_id = listEntry.list_id
        self.listEntry = listEntry

    def PerformAction(self, new_name):
        App.get_running_app().dataManip.ModifyList(self.list_id, new_name)

    def CloseAndReload(self, new_name):
        self.listEntry.name = new_name
        self.dismiss()


class DeleteTaskPopup(Popup):
    list_id = ''

    def __init__(self, list_id, **kwargs):
        super(DeleteTaskPopup, self).__init__(**kwargs)
        self.list_id = list_id

    def PerformAction(self):
        App.get_running_app().dataManip.DeleteList(self.list_id)

    def CloseAndReload(self):
        App.get_running_app().rootScr.ReloadListsView()
        self.dismiss()
