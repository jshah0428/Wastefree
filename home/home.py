from datetime import datetime

from login import loginbackend
from recieptScanner import process_receipt
import sqlite3
import databases_schema as dbs
import subprocess
import sys

# Kivy Imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.graphics import Color, Line, Rectangle


Window.size = (325, 600)
Window.clearcolor = (1, 0.94, 0.85, 1)

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
            font_size=34,
            font_name="Roboto",
            bold = "True",
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
            font_name="Roboto",
            bold=True
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

        pantry = Button(background_normal='images/pantry.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1), font_size=40)
        pantry.bind(on_press=self.switch_to_home_page)

        trends = Button(background_normal='images/trends.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        trends.bind(on_press=self.switch_to_trends_page)

        recipes = Button(background_normal='images/recipes.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        recipes.bind(on_press=self.switch_to_recipes_page)
        
        scan = Button(background_normal='images/scan.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        scan.bind(on_press=self.switch_to_scan_page)
        
        account = Button(background_normal='images/account.png', size_hint=(None, None), size=(60, 60), background_color=(0.133, 0.545, 0.133, 1))
        account.bind(on_press=self.logout)

        self.add_widget(pantry)
        self.add_widget(trends)
        self.add_widget(recipes)
        self.add_widget(scan)
        self.add_widget(account)

    # Upon activation of this function a popup will appear with a button saying "Logout", when pressed
    # the application will terminate 
    def logout(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Are you sure you want to logout?', halign='center', valign='middle', color=(0.133, 0.545, 0.133, 1)))

        logout_button = Button(text='Logout', size_hint=(1, 0.2), background_color=(0.133, 0.545, 0.133, 1))
        logout_button.bind(on_press=lambda x: self.terminate_app())
        layout.add_widget(logout_button)

        popup = Popup(title='Logout', content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def terminate_app(self):
        App.get_running_app().stop()
        Window.close()


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
        header = Label(text='Pantry', font_size=40, size_hint_y=None, bold=True, color=(0, 0.545, 0.137, 1))  # Green text
        self.add_widget(header)

        # New Button
        new_button = Button(
            text='New',
            font_size=34,
            size_hint=(0.1, 0.1), 
            background_color=(0, 0, 0, 0),  # Light green background

            color=(0.133, 0.545, 0.133, 1),  # Green text
            bold=True
        )
        
        def on_button_press(instance):
            with instance.canvas.before:
                Color(0, 0, 0, 0.3)  # Semi-transparent shadow color
                self.shadow = Rectangle(size=(instance.size[0] * 1.1, instance.size[1] * 1.1), pos=(instance.pos[0] - 5, instance.pos[1] - 5))

        def on_button_release(instance):
            instance.canvas.before.clear()

        new_button.bind(on_press=on_button_press)
        new_button.bind(on_release=on_button_release)

        new_button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        new_button.bind(on_press=self.new_entry)

        self.add_widget(new_button)

        # Scrollable Frame
        scroll_view = ScrollView()
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # for i in range(10):  # Example list entries
            # entry = ItemWidget(f'Item {i+1}', f'{i}', i)
            # scroll_layout.add_widget(entry)

        scroll_view.add_widget(scroll_layout)
        self.add_widget(scroll_view)

        self.NavBar = NavBar()
        self.add_widget(self.NavBar)

        connection = sqlite3.connect('/Users/shreyaskonanki/PycharmProjects/Wastefree/recipe.db')
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM pantry;")
        row_count = cursor.fetchone()[0]
        if row_count != 0:
            cursor.execute("""
                SELECT item_name, quantity, expiry_date, total_price
                FROM pantry
            """,)

            results = cursor.fetchall()  # Fetch all results


            for x in range(len(results)):
                new_item = ItemWidget(str(results[x][0]), str(results[x][1]), str(results[x][2]), str(results[x][3]))
                self.children[1].children[0].add_widget(new_item)

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

        avgCost_input = TextInput(hint_text='Unit Cost', multiline=False, padding_y=(20,20),
                             size_hint=(1, 0.5))
        layout.add_widget(avgCost_input)

        def add_item(instance):
            name = name_input.text
            quantity = quantity_input.text
            expire_date = datetime.strptime(expire_input.text, '%m/%d/%Y')
            expire = int(datetime(expire_date.year, expire_date.month, expire_date.day).timestamp())
            avgCost = float(avgCost_input.text) #supposed to be unit cost
            totalCost = avgCost*float(quantity)

            new_item = ItemWidget(name, quantity, expire, avgCost)
            self.children[1].children[0].add_widget(new_item)

            dbs.pantry_database()
            connection = sqlite3.connect('/Users/shreyaskonanki/PycharmProjects/Wastefree/recipe.db')
            cursor = connection.cursor()

            cursor.execute('''
            INSERT INTO pantry (item_name, quantity, unit_price, total_price, expiry_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (name, quantity, avgCost, totalCost, expire_date))

            connection.commit()
            connection.close()

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
        header = Label(
            text='Trends Page',
            size_hint_y=None,
            height=50,
            color=(0.0, 0.5, 0.0, 1)  # Dark green (RGBA)
        )
        self.add_widget(header)

        # Add the image (assuming you know the path)
        image_path = '../waste_price_plot.png'  # Replace with your actual file path
        image = Image(
            source=image_path,
            size_hint=(1.0, 1.0),  # Slightly larger image (default is 1.0)
            pos_hint={'center_x': 0.5, 'top': 0.9},  # Move higher (closer to the top)
        )
        self.add_widget(image)
        
        self.add_widget(NavBar())

class TrendsScreen(Screen):
    def __init__(self, **kwargs):
        super(TrendsScreen, self).__init__(**kwargs)
        self.add_widget(TrendsPage())

# Scanner Page
class ScannerPage(BoxLayout):
    def __init__(self, **kwargs):
        super(ScannerPage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Header Label
        header = Label(text='Receipt Scanner', bold=True, size_hint_y=None, height=50, color=(0, 0.545, 0.137, 1))
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
        header = Label(text='Return to pantry', size_hint_y=None, height=50, color=(0, 0.545, 0.137, 1), on_press=self.return_to_pantry )
        self.add_widget(header)
    
        for i in range(len(receipt_data[0])):
            self.show_popup(i)

        self.add_widget(NavBar())

    def return_to_pantry(self, instance):
        self.parent.parent.manager.current = 'HomePage'  # Navigate to the home page
    def show_popup(self, index):
        layout = GridLayout(cols=2, padding=10)

        name_input = TextInput(text=self.receipt_data[0][index])
        quantity_input = TextInput(text=str(self.receipt_data[1][index]))
        expiration_input = TextInput(text=str(self.receipt_data[2][index]))
        unit_cost_input = TextInput(text=str(self.receipt_data[3][index]))
        total_price = float(str(self.receipt_data[3][index]))*int(str(self.receipt_data[1][index]))

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
            expire_date = datetime.strptime(expiration_input.text, '%m/%d/%Y')

            dbs.pantry_database()
            connection = sqlite3.connect('/Users/shreyaskonanki/PycharmProjects/Wastefree/recipe.db')
            cursor = connection.cursor()


            cursor.execute('''
                    INSERT INTO pantry (item_name, quantity, unit_price, total_price, expiry_date)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (str(name_input.text), int(quantity_input.text), float(unit_cost_input.text), total_price, expire_date))

            connection.commit()
            connection.close()
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

# Recipes Page
class RecipesPage(BoxLayout):
    def __init__(self, **kwargs):
        super(RecipesPage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # RecipeApp().run()
        # # Header Label
        header = Label(text='Recipes Page', size_hint_y=None, height=50)
        self.add_widget(header)
        
        # Launch RecipeBook Button
        launch_button = Button(
            text='Launch RecipeBook',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        launch_button.bind(on_press=self.launch_recipe_book)
        self.add_widget(launch_button)

        self.add_widget(NavBar())
    def launch_recipe_book(self, instance):
        subprocess.Popen([sys.executable, '../recipe_finder/recipe_finder.py'])
class RecipesScreen(Screen):
    def __init__(self, **kwargs):
        super(RecipesScreen, self).__init__(**kwargs)
        self.add_widget(RecipesPage())


class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(HomeScreen(name='home_page'))
        sm.add_widget(TrendsScreen(name='trends_page'))
        sm.add_widget(ScannerScreen(name='scan_page'))
        sm.add_widget(RecipesScreen(name='recipes_page'))        

        return sm


if __name__ == '__main__':
    MyApp().run()