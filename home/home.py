from datetime import datetime 
from recieptScanner import process_receipt

# Kivy Imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
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
        infoButton = Button(size_hint=(None, None), size=(50, 50), background_normal='images/info.png', background_color=(0.133, 0.545, 0.133, 1), pos_hint={'center_x': 0.8, 'center_y': 0.5})
        infoButton.bind(on_press=lambda x: self.displayInformation())
        
        removeButton = Button(size_hint=(None, None), size=(50, 50), background_normal='images/remove.png', background_color=(0.133, 0.545, 0.133, 1), pos_hint={'center_x': 0.8, 'center_y': 0.5})
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

class NavBar(BoxLayout):
    def __init__(self, **kwargs):
        super(NavBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50
        self.padding = [40, 0]
        self.spacing = 10

        pantry = Button(background_normal='images/pantry.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        pantry.bind(on_press=self.switch_to_home_page)

        trends = Button(background_normal='images/trends.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        trends.bind(on_press=self.switch_to_trends_page)

        recipes = Button(background_normal='images/recipes.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        recipes.bind(on_press=self.switch_to_recipes_page)
        
        scan = Button(background_normal='images/scan.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        scan.bind(on_press=self.switch_to_scan_page)
        
        account = Button(background_normal='images/account.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))

        self.add_widget(pantry)
        self.add_widget(trends)
        self.add_widget(recipes)
        self.add_widget(scan)
        self.add_widget(account)

    def switch_to_home_page(self, instance):
        self.parent.parent.manager.current = 'home_page'
    
    def switch_to_trends_page(self, instance):
        self.parent.parent.manager.current = 'trends_page'
    
    def switch_to_recipes_page(self, instance):
        self.parent.parent.manager.current = 'recipes_page'
    
    def switch_to_scan_page(self, instance):
        self.parent.parent.manager.current = 'scan_page'

# Home Page
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
        new_button.bind(on_press=self.new_entry)

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

        self.NavBar = NavBar()
        self.add_widget(self.NavBar)


    def new_entry(self, instance):
        layout = BoxLayout(orientation='vertical')

        name_input = TextInput(hint_text='Name', multiline=False, padding_y=(20,20),
                             size_hint=(1, 0.5))
        layout.add_widget(name_input)

        quantity_input = TextInput(hint_text='Quantity', multiline=False, padding_y=(20,20),
                             size_hint=(1, 0.5))
        layout.add_widget(quantity_input)

        expire_input = TextInput(hint_text='Expiration Date (MM/DD/YYYY)', multiline=False, padding_y=(20,20),
                             size_hint=(1, 0.5))
        layout.add_widget(expire_input)

        avgCost_input = TextInput(hint_text='Average Cost', multiline=False, padding_y=(20,20),
                             size_hint=(1, 0.5))
        layout.add_widget(avgCost_input)

        def add_item(instance):
            name = name_input.text
            quantity = quantity_input.text
            expire_date = datetime.strptime(expire_input.text, '%m/%d/%Y')
            expire = int(datetime(expire_date.year, expire_date.month, expire_date.day).timestamp())
            avgCost = float(avgCost_input.text)

            foodId = 00000 # Convert
            individualID = 000000 # Convert
            
            new_item = ItemWidget(name, quantity, foodId, individualID, expire, avgCost)
            self.children[1].children[0].add_widget(new_item)

            # ADD TO DATABASE
            popup.dismiss()


        add_button = Button(text='Add',
                             size_hint=(1, 0.5))
        add_button.bind(on_press=add_item)
        layout.add_widget(add_button)

        popup = Popup(title='New Item',
              content=layout,
              size_hint=(0.8, 0.8))
        popup.open()
  
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.add_widget(HomePage())

# Trends Page
class TrendsPage(BoxLayout):
    def __init__(self, **kwargs):
        super(TrendsPage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Header Label
        header = Label(text='Trends Page', size_hint_y=None, height=50)
        self.add_widget(header)

        
        self.add_widget(NavBar())

class TrendsScreen(Screen):
    def __init__(self, **kwargs):
        super(TrendsScreen, self).__init__(**kwargs)
        self.add_widget(TrendsPage())

# Scanner Page
class ScannerPage(BoxLayout):
    def __init__(self, **kwargs):
        Window.clearcolor = (.2, .2, 0.2, 1) 
        super(ScannerPage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Header Label
        header = Label(text='Scanner Page', size_hint_y=None, height=50)
        self.add_widget(header)

        # FileChooser
        intial_path = './reciepts'
        self.file_chooser = FileChooserIconView( size_hint_y=None, height=500, path=intial_path)
        
         
        self.add_widget(self.file_chooser)

        # Submit Button
        submit_button = Button(text='Submit', size_hint_y=None, height=50)
        
        submit_button.bind(on_press=self.on_submit)
        self.add_widget(submit_button)

        self.add_widget(NavBar())

    # When submit is pressed, switch to a new page that takes in the ocr data
    # and prompts the user to confirm the data
    def on_submit(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            print(f"Selected file: {selected_file[0]}")
            receipt_data = process_receipt(selected_file[0])
            
            # item_adder_screen = ItemAdderScreen(receipt_data, name='item_adder_page')
            self.parent.manager.add_widget(ItemAdderScreen(receipt_data, name='item_adder_page'))
            self.parent.manager.current = 'item_adder_page'

        else:
            print("No file selected")

class ScannerScreen(Screen):
    def __init__(self, **kwargs):
        super(ScannerScreen, self).__init__(**kwargs)
        self.add_widget(ScannerPage())

# Item Adder Page, only appears after file submitted
class ItemAdderPage(BoxLayout): 
    def __init__(self, receipt_data, **kwargs):
        super(ItemAdderPage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.receipt_data = receipt_data

        # Header Label
        header = Label(text='Return to pantry', size_hint_y=None, height=50)
        self.add_widget(header)
    
        for i in range(len(receipt_data[0])):
            self.show_popup(i)

        self.add_widget(NavBar())


    def show_popup(self, index):
        layout = GridLayout(cols=2, padding=10)

        name_input = TextInput(text=self.receipt_data[0][index])
        quantity_input = TextInput(text=str(self.receipt_data[1][index]))
        expiration_input = TextInput(text=str(self.receipt_data[2][index]))
        unit_cost_input = TextInput(text=str(self.receipt_data[3][index]))

        layout.add_widget(Label(text='Name:'))
        layout.add_widget(name_input)
        layout.add_widget(Label(text='Quantity:'))
        layout.add_widget(quantity_input)
        layout.add_widget(Label(text='Expiration Date:'))
        layout.add_widget(expiration_input)
        layout.add_widget(Label(text='Unit Cost:'))
        layout.add_widget(unit_cost_input)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        add_button = Button(text='Add')
        remove_button = Button(text='Remove')

        button_layout.add_widget(add_button)
        button_layout.add_widget(remove_button)

        layout.add_widget(button_layout)

        popup = Popup(title='Edit Item', content=layout, size_hint=(0.8, 0.8))
        popup.open()

        def add_item(index):
            # Logic to add the item
            popup.dismiss()
            
        def remove_item():
            # Logic to remove the item
            popup.dismiss()
        add_button.bind(on_press=lambda x: add_item(index))
        remove_button.bind(on_press=lambda x: remove_item())   
        

class ItemAdderScreen(Screen):
    def __init__(self, reciept_data, **kwargs):
        super(ItemAdderScreen, self).__init__(**kwargs)
        self.add_widget(ItemAdderPage(reciept_data))


class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(HomeScreen(name='home_page'))
        sm.add_widget(TrendsScreen(name='trends_page'))
        sm.add_widget(ScannerScreen(name='scan_page'))
        
        # Add widgets for the different screens

        return sm


if __name__ == '__main__':
    MyApp().run()