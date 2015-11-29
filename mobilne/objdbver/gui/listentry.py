from kivy.app import App
from kivy.properties import StringProperty
from popups import InfoPopup, ServReqPopup, EditListPopup, DeleteListPopup
from kivy.uix.button import Button

class ListEntry(Button):
    name = StringProperty()
    list_id = ''

    def __init__(self, list_id = '0', name = 'zadanie', **kwargs):
        # print('init with {z} id - {i}'.format(z=name, i = list_id))
        self.name = name
        self.list_id = list_id
        super(ListEntry, self).__init__(**kwargs)

    def show_edit_list(self):
        p = EditListPopup(self)
        p.open()

    def show_popup(self):
        p = CustomPopup(self.list_id)
        p.open()

    def show_confirm_list_del(self):
        p = DeleteListPopup(self.list_id)
        p.open()

    def PickListAction(self):
        app = App.get_running_app()
        app.ListTaskPickAction(self.list_id)
