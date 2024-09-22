from datetime import datetime 

# Kivy Imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.graphics import Color, Line

Window.size = (325, 600)
Window.clearcolor = (1, 1, 1, 1)  # White background

#TODO
# - FIX THE UI DOING THAT
# - Fix the UI so it doesnt look stupid
# - Add functionality to buttons
# - Load from data base function
# - To handle item removals/update what we need to do is 
#   make sure that the item is updated in the data base first,
#   and then while loading 
#   and for new items 
#   During preprocessing stage, display notifications for expired items
#   For the new button, add in a expiry date

class ItemWidget(BoxLayout):
    def __init__(self, name, quantity, foodId, individualID=0000, expire=1729543021, avgCost=5.0):
        super(ItemWidget, self).__init__()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 100
        self.padding = [10, 10, 10, 10]
        self.spacing = 10

        self.name = name
        self.quantity = quantity
        self.foodId = foodId
        self.individualID = individualID
        self.expire = expire
        self.avgCost = avgCost

        # Updated colors for the new eco-friendly theme
        self.primary_color = (0.133, 0.545, 0.133, 1)  # Green text
        self.secondary_color = (0.133, 0.545, 0.133, 1)  # Green text

        # Food Name Label with environmental style
        self.entry_name = Label(
            text=name, 
            size_hint_x=2,
            halign='left', 
            valign='middle',
            color=self.primary_color, 
            font_size=18,
            font_name="Roboto"
        )
        self.entry_name.bind(size=self.entry_name.setter('text_size'))

        # Food Quantity Label
        self.entry_number = Label(
            text=quantity, 
            size_hint_x=1, 
            halign='right', 
            valign='middle',
            color=self.secondary_color, 
            font_size=18,
            font_name="Roboto"
        )
        self.entry_number.bind(size=self.entry_number.setter('text_size'))

        # Info and Remove Buttons
        infoButton = Button(size_hint=(None, None), size=(50, 50), background_normal='images/info.png', background_color=(0.133, 0.545, 0.133, 1))
        infoButton.bind(on_press=lambda x: self.displayInformation())
        
        removeButton = Button(size_hint=(None, None), size=(50, 50), background_normal='images/remove.png', background_color=(0.133, 0.545, 0.133, 1))
        removeButton.bind(on_press=lambda x: self.consumeFood())

        # Add widgets
        self.add_widget(self.entry_name)
        self.add_widget(self.entry_number)
        self.add_widget(infoButton)
        self.add_widget(removeButton)

    def consumeFood(self):
        print('Removing food')

        def remove_quantity(instance):
            quantity_to_remove = int(quantity_input.text)
            self.quantity = str(max(0, int(self.quantity) - quantity_to_remove))
            self.entry_number.text = self.quantity
            popup.dismiss()

            if int(self.quantity) == 0:
                self.parent.remove_widget(self)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=f'Remove {self.name}(s)\nCurrent Quantity: {self.quantity}', halign='center', valign='middle', color=self.primary_color))
        quantity_input = TextInput(multiline=False, hint_text='Enter quantity to remove')
        layout.add_widget(quantity_input)

        remove_button = Button(text='Remove', size_hint=(1, 0.2), background_color=(0.133, 0.545, 0.133, 1))
        remove_button.bind(on_press=remove_quantity)
        layout.add_widget(remove_button)

        popup = Popup(title='Remove Quantity', content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def displayInformation(self):
        date_time = datetime.fromtimestamp(self.expire)
        formatted_date = date_time.strftime('%m/%d/%Y')
        totalcost = int(self.quantity) * float(self.avgCost)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=f'Name: {self.name}', color=self.primary_color, font_size=18))
        layout.add_widget(Label(text=f'Quantity: {self.quantity}', color=self.secondary_color, font_size=18))
        layout.add_widget(Label(text=f'Expiration: {formatted_date}', color=self.primary_color, font_size=18))
        layout.add_widget(Label(text=f'Total Cost: ${totalcost:.2f}', color=self.secondary_color, font_size=18))

        close_button = Button(text='Close', size_hint=(1, 0.2), background_color=(0.133, 0.545, 0.133, 1))
        close_button.bind(on_press=lambda x: popup.dismiss())
        layout.add_widget(close_button)

        popup = Popup(title='Item Information', content=layout, size_hint=(0.8, 0.5))
        popup.open()


class HomePage(BoxLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Header Label
        header = Label(text='Pantry', font_size=24, size_hint_y=None, bold=True, color=(0, 0.545, 0.137, 1))  # Green text
        self.add_widget(header)

        # New Button
        new_button = Button(
            text='New', 
            size_hint=(0.1, 0.1), 
            background_color=(0, 0, 0, 0),  # Light green background
            color=(0.133, 0.545, 0.133, 1)  # Green text
        )
        new_button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(new_button)

        # Scrollable Frame
        scroll_view = ScrollView()
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        for i in range(10):  # Example list entries
            entry = ItemWidget(f'Item {i+1}', f'{i}', i)
            scroll_layout.add_widget(entry)

        scroll_view.add_widget(scroll_layout)
        self.add_widget(scroll_view)

        # Navigation Bar
        nav_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=[45, 0], spacing=20)

        pantry = Button(background_normal='images/pantry.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        trends = Button(background_normal='images/trends.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        recipes = Button(background_normal='images/recipes.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        account = Button(background_normal='images/account.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))

        nav_bar.add_widget(pantry)
        nav_bar.add_widget(trends)
        nav_bar.add_widget(recipes)
        nav_bar.add_widget(account)

        self.add_widget(nav_bar)


class NewPage(BoxLayout):
    def __init__(self, **kwargs):
        super(NewPage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Header Label
        header = Label(text='New Page', size_hint_y=None, height=50)
        self.add_widget(header)

        # Back Button
        back_button = Button(text='Back', size_hint_y=None, height=50)
        back_button.bind(on_press=self.switch_to_home_page)
        self.add_widget(back_button)

    def switch_to_home_page(self, instance):
        self.parent.current = 'home_page'


class MyApp(App):
    def build(self):
        sm = ScreenManager()

        home_page = HomePage()
        screen_home = Screen(name='home_page')
        screen_home.add_widget(home_page)
        sm.add_widget(screen_home)

        new_page = NewPage()
        screen_new = Screen(name='new_page')
        screen_new.add_widget(new_page)
        sm.add_widget(screen_new)

        return sm


if __name__ == '__main__':
    MyApp().run()