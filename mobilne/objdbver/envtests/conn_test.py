from kivy.uix.widget import Widget
from kivy.app import App
from kivy.network.urlrequest import UrlRequest

class EventTest(App):
    def redirAct(self, req,res):
        print("redir")

    def success(self, event, msg):
        print("success")
        print(msg)

    #this version fails the most consistently, the naked urlrequest
    def build(self):
        self.q = UrlRequest("http://wp.pl", self.success, on_redirect=self.redirAct)
        return Widget()

EventTest().run()
