from kivy.app import App
from kivy.properties import StringProperty
from popups import InfoPopup, ServReqPopup, EditTaskPopup, DeleteTaskPopup
from kivy.uix.button import Button

class TaskEntry(Button):
    name = StringProperty()
    task_id = ''
    priority = -1

    def __init__(self, task_id = '0', name = 'zadanie', prior = 1, **kwargs):
        print('init task with {z} id - {i} (prior{p})'.format(z=name, \
                i = task_id, p = prior))
        self.name = name
        self.task_id = task_id
        self.priority = prior
        super(TaskEntry, self).__init__(**kwargs)

    def show_edit_list(self):
        p = EditTaskPopup(self)
        p.open()

    def show_popup(self):
        p = CustomPopup(self.task_id)
        p.open()

    def show_confirm_list_del(self):
        p = DeleteTaskPopup(self.task_id)
        p.open()

    def PickListAction(self):
        app = App.get_running_app()
        app.ListTaskPickAction(self.task_id)
