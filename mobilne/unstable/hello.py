# from kivy.app import App
# from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest

# class TutorialApp(App):
# 	def build(self):
# 		return Button(text='Hello!',
#                       background_color=(0, 0, 1, 1),  # List of
#                                                       # rgba components
#                       font_size=150)

def got_pomidor(req, results):
    #for key, value in results['weather'][0].items():
    #    print(key, ': ', value)
    print("dupa")
    print(results)

def got_weather(req, results):
    for key, value in results['weather'][0].items():
        print(key, ': ', value)

if __name__ == "__main__":
#	TutorialApp().run()

#	req = UrlRequest(
#	    'http://tomato-cal.herokuapp.com/lists.json',
#	    got_pomidor)
	req = UrlRequest(
	    'http://api.openweathermap.org/data/2.5/weather?q=Paris,fr',
	    got_weather)

def do_req():
	req = UrlRequest(
	    'http://api.openweathermap.org/data/2.5/weather?q=Paris,fr',
	    got_weather)
	return req
