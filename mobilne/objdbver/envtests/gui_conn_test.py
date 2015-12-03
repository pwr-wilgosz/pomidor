from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label

class ShowyLabel(Label):
    def get_input(self, *args):
        print 'did get_input!'
        print 'args are', args
        self.text = str(args)
    def got_weather(self, req, results):
        for key, value in results['weather'][0].items():
            print(key, ': ', value)

root = Builder.load_string('''
#:import UrlRequest kivy.network.urlrequest.UrlRequest
#:import partial functools.partial
BoxLayout:
    orientation: 'vertical'
    ShowyLabel:
        id: lab
        text: 'empty'
        text_size: self.size
    TextInput:
        id: ti
        text: 'http://inclem.net'
    Button:
        on_release: UrlRequest(ti.text, partial(lab.get_input, 'success'), partial(lab.get_input, 'redirect'), partial(lab.get_input, 'failure'), partial(lab.get_input, 'error'), partial(lab.get_input, 'progress'))
        # on_press: UrlRequest('http://api.openweathermap.org/data/2.5/weather?q=Paris,fr', lab.got_weather)
''')

runTouchApp(root)
