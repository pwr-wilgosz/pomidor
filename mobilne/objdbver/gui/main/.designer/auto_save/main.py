from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App


class RootWidget(FloatLayout):
    lists_content=ObjectProperty(None)
    tasks_content=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.lists_content.bind(minimum_height=self.lists_content.setter('height'))
        self.tasks_content.bind(minimum_height=self.tasks_content.setter('height'))
    '''This is the class representing your root widget.
       By default it is inherited from BoxLayout,
       you can use any other layout/widget depending on your usage.
    '''


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

if '__main__' == __name__:
    MainApp().run()
