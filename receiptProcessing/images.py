from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MyWidget(GridLayout):
    def __init__(self, callback, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.cols = 2
        self.callback = callback

    def selected(self, filename):
        print("Selected file:", filename[0])
        # Send the selected filename to the callback
        self.callback(filename[0])

    def send_image_to_processor(self, filename):
        print("Image sent to processor:", filename)
        return filename

class FileChooserWindow(App):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    def build(self):
        return MyWidget(callback=self.callback)

if __name__ == "__main__":
    window = FileChooserWindow()
    window.run()