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
from kivy.core.window import Window
Window.size = (325, 600)

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

        self.name = name
        self.quantity = quantity
        self.foodId = foodId
        self.individualID = individualID
        self.expire = expire
        self.avgCost = avgCost

       
        # Food Name
        self.entry_name     = Label( 
                                text=name, 
                                size_hint_x=1, 
                                width=100)
        #Food Quantity
        self.entry_number   = Label(
                                text=quantity, 
                                size_hint_x=1,
                                width=10)
        

        # Info Button
        infoButton = Button(size_hint=(0.8,0.8), background_normal='images/info.png')
        infoButton.bind(on_press=lambda x: self.displayInformation())

        # Remove Button
        removeButton = Button(size_hint_x=0.6, background_normal='images/remove.png')
        removeButton.bind(on_press=lambda x: self.consumeFood())

        # Adding widgets
        self.add_widget(self.entry_name)
        self.add_widget(self.entry_number)
        self.add_widget(infoButton)
        self.add_widget(removeButton)
    
    # If the quantity is 0, remove the item from the list 
    def consumeFood(self):
        # Create a popup which asks how much to remove or all
        print('Removing food')
        def remove_quantity(instance):
            quantity_to_remove = int(quantity_input.text)
            self.quantity = str(max(0, int(self.quantity) - quantity_to_remove))
            self.entry_number.text = self.quantity
            popup.dismiss()

            # MAKE SURE TO UPDATE THE DATA BASE FIRST THOUGH
            if int(self.quantity) == 0:
                self.parent.remove_widget(self)            

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=f'{self.quantity} {self.name}(s)\nHow many do you want to remove? ',
                    halign='center', valign='middle', text_size=(None, None)))
        quantity_input = TextInput(multiline=False)
        layout.add_widget(quantity_input)

        remove_button = Button(text='Remove')
        remove_button.bind(on_press=remove_quantity)
        layout.add_widget(remove_button)

        popup = Popup(title='Remove Quantity',
                  content=layout,
                  size_hint=(0.8, 0.5))
        popup.open()


    def displayInformation(self):
        # Create a popup which displays the information about the item
        date_time = datetime.fromtimestamp(self.expire)
        formatted_date = date_time.strftime('%m/%d/%Y')
        totalcost = int(self.quantity) * float(self.avgCost)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=f'Name: {self.name}', size_hint=(1, 0.2), halign='center', valign='middle', text_size=(None, None)))
        layout.add_widget(Label(text=f'Quantity: {self.quantity}', size_hint=(1, 0.2), halign='center', valign='middle', text_size=(None, None)))
        layout.add_widget(Label(text=f'Expiration: {formatted_date}', size_hint=(1, 0.2), halign='center', valign='middle', text_size=(None, None)))
        layout.add_widget(Label(text=f'Total Cost: ${format(totalcost, ",.2f")}', size_hint=(1, 0.2), halign='center', valign='middle', text_size=(None, None)))
        

        close_button = Button(text='Close', size_hint=(1, 0.2))
        close_button.bind(on_press=lambda x: popup.dismiss())
        layout.add_widget(close_button)

        popup = Popup(title='Item Information',
                      content=layout,
                      size_hint=(0.8, 0.5))
        popup.open()


# Home Page
class HomePage(BoxLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Header Label
        header = Label(text='Pantry', font_size=24, size_hint_y=None, bold=True) # Might need to add a size thing here
        self.add_widget(header)

        # New Button
        new_button = Button(text='New', size_hint = (0.4, 0.1))
        new_button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(new_button)

        # Scrollable Frame
        scroll_view = ScrollView()
        #scroll_view = ScrollView(size_hint=(1, None), size=(self.width, 300))
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
    

        for i in range(10):  # Example list entries
            entry = ItemWidget(f'Item {i+1}', f'{i}', i)
            scroll_layout.add_widget(entry)

        scroll_view.add_widget(scroll_layout)
        self.add_widget(scroll_view)

        
        nav_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        pantry= Button(background_normal='images/pantry.png')
        nav_bar.add_widget(pantry)

        trends= Button(size_hint_x=1, width=100, background_normal='images/trends.png')
        nav_bar.add_widget(trends)

        recipes= Button(size_hint_x=1, width=100, background_normal='images/recipes.png')
        nav_bar.add_widget(recipes)

        account= Button(size_hint_x=1, width=100, background_normal='images/account.png')
        nav_bar.add_widget(account)
                
        self.add_widget(nav_bar)
        
       


# Page Management 
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


# Core App
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




