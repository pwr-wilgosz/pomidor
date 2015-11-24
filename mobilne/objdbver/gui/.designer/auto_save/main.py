from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
#from kivy.core.window import Window
#Window.size = (480, 255)

class RootWidget(FloatLayout):
    lists_content=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.lists_content.bind(minimum_height=self.lists_content.setter('height'))
        self.lists_content.add_widget(ListEntry())
    '''This is the class representing your root widget.
       By default it is inherited from BoxLayout,
       you can use any other layout/widget depending on your usage.
    '''

class EditTaskPopup(Popup):
    pass

class DeleteTaskPopup(Popup):
    pass

class ListEntry(Button):
    pass

class MainApp(App):
    '''This is the main class of your app.
       Define any app wide entities here.
       This class can be accessed anywhere inside the kivy app as,
       in python::

         app = App.get_running_app()
         print (app.title)

       in kv language::

         on_release: print(app.title)
       Name of the .kv file that is auto-loaded is derived from the name
       of this class::

         MainApp = main.kv
         MainClass = mainclass.kv

       The App part is auto removed and the whole name is lowercased.
    '''

    def build(self):
        return RootWidget()

    def show_popup(self, b):
        p = CustomPopup()
        p.open()

    def show_edit_list(b):
        p = EditTaskPopup()
        p.open()

    def show_confirm_list_del(b):
        p = DeleteTaskPopup()
        p.open()

if '__main__' == __name__:
    MainApp().run()
