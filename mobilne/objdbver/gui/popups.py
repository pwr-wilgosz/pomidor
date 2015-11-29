# -*- coding: utf-8 -*-
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.dropdown import DropDown
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

class EditListPopup(Popup):
    list_id = ''
    listEntry = None

    def __init__(self, listEntry, **kwargs):
        super(EditListPopup, self).__init__(**kwargs)
        self.list_id = listEntry.list_id
        self.listEntry = listEntry

    def PerformAction(self, new_name):
        App.get_running_app().dataManip.ModifyList(self.list_id, new_name)

    def CloseAndReload(self, new_name):
        self.listEntry.name = new_name
        self.dismiss()

class DeleteListPopup(Popup):
    list_id = ''

    def __init__(self, list_id, **kwargs):
        super(DeleteListPopup, self).__init__(**kwargs)
        self.list_id = list_id

    def PerformAction(self):
        App.get_running_app().dataManip.DeleteList(self.list_id)

    def CloseAndReload(self):
        App.get_running_app().rootScr.ReloadListsView()
        self.dismiss()

class PriorityDropDown(DropDown):
    chosenPrio = 0

    def __init__(self, **kwargs):
        super(PriorityDropDown, self).__init__(**kwargs)

    def MySelect(self, number, text):
        self.chosenPrio = number
        self.select(text)

class CreateTaskPopup(Popup):
    priority = 1
    cycleLabel = StringProperty()

    def __init__(self, prior, **kwargs):
        self.priority = prior
        self.dropdown = PriorityDropDown()
        self.title = 'Dodwanie zadania o priorytecie {p}'.\
                    format(p = self.NameOfPriority(prior))
        self.UpdateLabel(3)
        super(CreateTaskPopup, self).__init__(**kwargs)

    def NameOfPriority(self, prior):
        return {
            1: 'ważne - pilne',
            2: 'nie ważne - pilne',
            3: 'ważne - nie pilne',
        }.get(prior, 'nie ważne - nie pilne')

    def UpdateLabel(self, value):
        value = int(value)
        self.cycleLabel = 'Zakładana ilość cykli ({c})'.\
                    format(c=value)

    def PerformAction(self, name, dur):
        dur = int(dur)
        App.get_running_app().dataManip.SubmitTask(name, self.priority, dur)

    def CloseAndReload(self):
        App.get_running_app().rootScr.ReloadTasksView()
        self.dismiss()

class EditTaskPopup(Popup):
    task_obj = None
    dropdown = None
    dropButton = ObjectProperty(None)
    durSlider = ObjectProperty(None)
    cycleLabel = StringProperty()

    def __init__(self, task_obj, **kwargs):
        self.task_obj = task_obj
        self.dropdown = PriorityDropDown()
        self.title = 'Edycja zadania "{t}"'.\
                    format(t=task_obj.name)
        super(EditTaskPopup, self).__init__(**kwargs)
        self.durSlider.value=task_obj.duration
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.dropButton, 'text', x))

    def UpdateLabel(self, value):
        value = int(value)
        self.cycleLabel = 'Zakładana ilość cykli ({c})'.\
                    format(c=value)


    def PerformAction(self, new_name):
        new_prior = None
        if self.dropdown.chosenPrio != 0:
            new_prior = self.dropdown.chosenPrio
        new_duration = int(self.durSlider.value)

        App.get_running_app().dataManip.ModifyTask(self.task_obj.task_id, \
            new_name, new_duration, new_prior)

    def CloseAndReload(self, new_name):
        App.get_running_app().rootScr.ReloadTasksView()

        self.dismiss()

class DeleteTaskPopup(Popup):
    task_id = ''

    def __init__(self, task_id, **kwargs):
        super(DeleteTaskPopup, self).__init__(**kwargs)
        self.task_id = task_id

    def PerformAction(self):
        App.get_running_app().dataManip.DeleteTask(self.task_id)

    def CloseAndReload(self):
        App.get_running_app().rootScr.ReloadTasksView()
        self.dismiss()
