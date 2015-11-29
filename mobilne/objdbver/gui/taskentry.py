from kivy.app import App
from kivy.properties import StringProperty
from popups import InfoPopup, EditTaskPopup, DeleteTaskPopup
from kivy.uix.button import Button

class TaskEntry(Button):
    name = StringProperty()
    task_id = ''
    priority = -1
    duration = 0

    def __init__(self, task_id = '0', name = 'zadanie', prior = 1,\
                duration = 0, **kwargs):
        print('init task with {z} id - {i} (prior: {p}, dur: {d})'.format(z=name, \
                i = task_id, p = prior, d = duration))
        self.name = name
        self.task_id = task_id
        self.priority = prior
        self.duration = duration
        super(TaskEntry, self).__init__(**kwargs)

    def show_edit_task(self):
        p = EditTaskPopup(self)
        p.open()

    def show_popup(self):
        p = CustomPopup(self.task_id)
        p.open()

    def show_confirm_task_del(self):
        p = DeleteTaskPopup(self.task_id)
        p.open()

    def PickTaskAction(self):
        app = App.get_running_app()
        app.ListTaskPickAction(task_id = self.task_id)
