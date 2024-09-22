'''
one with statistics on how much food you have wasted over time (in unit cost - aggregate that)
money spent on groceries over time
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import matplotlib.pyplot as plt
import numpy as np

class MatplotlibGraphApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Create a Matplotlib figure
        plt.figure()
        plt.plot(x, y, label='Sine Wave')
        plt.title('Matplotlib Graph in Kivy')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.legend()

        # Save the figure to a file
        plt.savefig('plot.png')
        plt.close()

        # Load the image and add it to the layout
        img = Image(source='plot.png')
        layout.add_widget(img)

        return layout

if __name__ == '__main__':
    MatplotlibGraphApp().run()
