from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
import webbrowser
import requests
from bs4 import BeautifulSoup
import json
from PIL import Image
from io import BytesIO
import certifi
import sqlite3
from kivymd.uix.boxlayout import MDBoxLayout
import databases_schema as dbs

class GreenOneLineListItem(OneLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = [0.133, 0.545, 0.133, 0.3] # Green background
        self.text_color = get_color_from_hex("#FFFFFF")  # White text
        self.font_style = "H6"

KV = '''
ScreenManager:
    SearchScreen:
    RecipeListScreen:
    RecipeDetailScreen:

<GreenOneLineListItem@OneLineListItem>:
    bg_color: 0.133, 0.545, 0.133, 1  # Green background
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1  # White text

<SearchScreen>:
    name: 'search'
    Image:
        source: '../login/BackgroundPic.png'
        allow_stretch: True
        keep_ratio: False

    MDBoxLayout:
        orientation: 'vertical'
        spacing: 10

        MDRaisedButton:
            text: "Saved Recipes"
            on_release: app.display_saved_recipes()
            pos_hint: {"center_x": .5}
            md_bg_color: 0.133, 0.545, 0.133, 1  # Green background (RGBA)
            text_color: 1, 1, 1, 1   # White text (RGBA)

        MDScrollView:
            size_hint_y: 0.3  # Adjust this value to control the height of the scroll area
            MDList:
                id: saved_recipes_list

        MDTopAppBar:
            title: "Recipe Search"
            elevation: 10
            md_bg_color: 0.133, 0.545, 0.133, 1  # green background (RGBA)
            text_color: 1, 1, 1, 1   # White text (RGBA)

        MDTextField:
            id: search_field
            hint_text: "Enter ingredients..."
            mode: "rectangle"
            size_hint_x: None
            width: "300dp"
            pos_hint: {"center_x": .5}
            line_color_normal: 0.133, 0.545, 0.133, 1  # Green border color
            line_color_focus: 0.133, 0.545, 0.133, 1  # Green border color when focused
            text_color_normal: 0.133, 0.545, 0.133, 1  # Green text color
            text_color_focus: 0.133, 0.545, 0.133, 1  # Green text color when focused
            hint_text_color_normal: 0.133, 0.545, 0.133, 0.7  # Green hint text color (slightly transparent)
            hint_text_color_focus: 0.133, 0.545, 0.133, 0.7  # Green hint text color when focused

        MDRaisedButton:
            text: "Search Recipes"
            pos_hint: {"center_x": .5}
            on_release: app.search_recipes()
            md_bg_color: 0.133, 0.545, 0.133, 1  # Green background (RGBA)
            text_color: 1, 1, 1, 1   # White text (RGBA)
<RecipeListScreen>:
    name: 'recipe_list'
    Image:
        source: '../login/BackgroundPic.png'
        allow_stretch: True
        keep_ratio: False
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Recipe List"
            left_action_items: [["arrow-left", lambda x: app.switch_screen('search')]]
            md_bg_color: 0.133, 0.545, 0.133, 1  # green background (RGBA)
            text_color: 1, 1, 1, 1   # White text (RGBA)
            
        MDLabel:
            id: save_message
            text: ""
            halign: "center"
            theme_text_color: "Custom"
            md_bg_color: 0.133, 0.545, 0.133, 1  # Red background (RGBA)
            text_color: 1, 1, 1, 1   # White text (RGBA)
            size_hint_y: None
            height: self.texture_size[1]
            

        MDScrollView:
            MDList:
                id: recipe_list

<RecipeDetailScreen>:
    name: 'recipe_detail'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Recipe Details"
            md_bg_color: 0.133, 0.545, 0.133, 1  # Red background (RGBA)
            text_color: 1, 1, 1, 1   # White text (RGBA)
            left_action_items: [["arrow-left", lambda x: app.switch_screen('recipe_list')]]

        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: dp(20)
                spacing: dp(10)

                

                MDLabel:
                    id: recipe_name
                    font_style: "H5"
                    halign: "center"

                MDRaisedButton:
                    id: recipe_link
                    text: "View Original Recipe"
                    md_bg_color: 0.133, 0.545, 0.133, 1  # green background (RGBA)
                    text_color: 1, 1, 1, 1   # White text (RGBA)
                    pos_hint: {"center_x": .5}
                    on_release: app.open_recipe_link()

                MDLabel:
                    id: recipe_description
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    text: "Ingredients:"
                    font_style: "H6"

                MDLabel:
                    id: recipe_ingredients
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    text: "Directions:"
                    font_style: "H6"

                MDLabel:
                    id: recipe_directions
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    text: "Nutrition Facts:"
                    font_style: "H6"

                MDLabel:
                    id: recipe_nutrition
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    text: "Preparation Info:"
                    font_style: "H6"

                MDLabel:
                    id: recipe_prep_info
                    size_hint_y: None
                    height: self.texture_size[1]
'''

class SearchScreen(Screen):
    pass

class RecipeListScreen(Screen):
    pass

class RecipeDetailScreen(Screen):
    pass

class RecipeApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.current_recipe_url = None
        return Builder.load_string(KV)

    def switch_screen(self, screen_name):
        self.root.current = screen_name
        if screen_name == 'search':
            self.display_saved_recipes()

    def search_recipes(self):
        first_page = self.root.get_screen('search')
        search_text = first_page.ids.search_field.text
        recipes = self.scraper(search_text)
        self.display_recipe_list(recipes)

    def display_saved_recipes(self):
        connection = sqlite3.connect('/Users/jainamshah/PycharmProjects/Wastefree/recipe.db')

        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SAVED_RECIPES'")
        table_exists = cursor.fetchone()

        search_screen = self.root.get_screen('search')
        saved_recipes_list = search_screen.ids.saved_recipes_list
        saved_recipes_list.clear_widgets()  # Clear existing widgets

        if table_exists:
            cursor.execute("SELECT DISTINCT RECIPE_NAME, RECIPE_URL FROM SAVED_RECIPES")
            saved_recipes = cursor.fetchall()

            if saved_recipes:
                for recipe in saved_recipes:
                    item = GreenOneLineListItem(
                        text=recipe[0],
                        on_release=lambda x, url=recipe[1]: webbrowser.open(url)
                    )
                    saved_recipes_list.add_widget(item)
            else:
                saved_recipes_list.add_widget(GreenOneLineListItem(text="No saved recipes"))
        else:
            saved_recipes_list.add_widget(GreenOneLineListItem(text="No saved recipes"))

        connection.close()





    def scraper(self, search_text):
        food_list = search_text.split()

        recipe_variables = {}
        for x in range(len(food_list)):
            recipe_variables[f'food_item{x}'] = food_list[x]

        if len(recipe_variables) == 1:
            url = f'https://www.allrecipes.com/search?q={recipe_variables["food_item0"]}'
        else:
            recipe_string = ''
            for x in range(len(recipe_variables)):
                if x != len(recipe_variables)-1:
                    recipe_string += recipe_variables[f'food_item{x}']+'+'
                else:
                    recipe_string += recipe_variables[f'food_item{x}']

            url = f'https://www.allrecipes.com/search?q={recipe_string}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html')

        title_elements = soup.find_all('span', class_="card__title-text")

        anchor_elements = soup.find_all('a',
                                        class_="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image")
        list_of_href_elements = []
        for a in anchor_elements:
            list_of_href_elements.append(a.get('href'))

        recipes = []
        for counter, a in enumerate(title_elements):
            recipe = {}
            recipe['name'] = a.getText()
            recipe['url'] = list_of_href_elements[counter]

            url_dish = list_of_href_elements[counter]
            response2 = requests.get(url_dish, verify=certifi.where())
            soup2 = BeautifulSoup(response2.text, 'html')
            script = soup2.find_all('script')[2].text.strip()

            data = json.loads(script)
            recipe['ingredients'] = data[0]['recipeIngredient']



            description = soup2.findAll("p", class_="comp mntl-sc-block mntl-sc-block-html")
            try:
                description_title = soup2.find('h2',
                                               class_='comp mntl-sc-block allrecipes-sc-block-heading mntl-sc-block-heading')
                title = description_title.get_text()
                title_list = title.split()
                title_final1 = title_list[len(title_list) - 2] + ' ' + title_list[len(title_list) - 1]
                title_final1 = title_final1.strip('!?/*')

                title_final2 = title_list[len(title_list) - 2] + ' ' + title_list[len(title_list) - 1].lower()
                title_final2 = title_final2.strip('!?/\*')

                title_final3 = title_list[len(title_list) - 2].lower() + ' ' + title_list[len(title_list) - 1].lower()
                title_final3 = title_final3.strip('!?/\*')

                for p in description:
                    if title_final1 in p.get_text() or title_final2 in p.get_text() or title_final3 in p.get_text():
                        recipe['description'] = p.get_text(strip=True)
                        break
                else:
                    recipe['description'] = "Description unavailable"
            except AttributeError:
                recipe['description'] = "Description unavailable"

            directions = soup2.find("div", id="mm-recipes-steps__content_1-0")
            directions_list = directions.find('ol')
            recipe['directions'] = [li.find('p', recursive=False).get_text() for li in directions_list.findAll('li')]

            table = soup2.find('table', class_="mm-recipes-nutrition-facts-summary__table")
            table_data = []
            for row in table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                table_data.append('\t'.join(row_data))
            recipe['nutrition'] = table_data

            div_prep = soup2.find('div', class_="mm-recipes-details__content")
            div_prep_formatted = []
            for div in div_prep.find_all('div', recursive=False):
                div_prep_text = [d.getText(strip=True) for d in div]
                div_prep_formatted.append('\t'.join(div_prep_text))
            recipe['prep_info'] = div_prep_formatted

            recipes.append(recipe)

            if counter == 4:  # Limit to 5 recipes
                break

        return recipes

    #page where we see all recipe list and save button
    def display_recipe_list(self, recipes):
        recipe_list = self.root.get_screen('recipe_list').ids.recipe_list
        recipe_list.clear_widgets()

        for recipe in recipes:
            # Create a horizontal layout (BoxLayout) for each recipe item
            box_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height='48dp')

            # Create the recipe list item (OneLineListItem)
            item = GreenOneLineListItem(text=recipe['name'], on_release=lambda x, r=recipe: self.show_recipe_detail(r))

            # Create the green "Save" button
            save_button = MDRaisedButton(
                text="Save",
                md_bg_color= (0.133, 0.545, 0.133, 1),  # Green background color (RGBA format)
                on_release=lambda x, r=recipe: self.save_recipe(r)  # Call save method when pressed
            )

            # Add the item and save button to the box layout
            box_layout.add_widget(item)
            box_layout.add_widget(save_button)

            # Add the box layout to the recipe list
            recipe_list.add_widget(box_layout)

        self.switch_screen('recipe_list')
    def show_recipe_detail(self, recipe):
        detail_screen = self.root.get_screen('recipe_detail')
        detail_screen.ids.recipe_name.text = recipe['name']
        # detail_screen.ids.recipe_image.source = recipe['image_url']  # Set the image source
        # detail_screen.ids.recipe_image.reload()  # Reload the image
        detail_screen.ids.recipe_description.text = recipe['description']
        detail_screen.ids.recipe_ingredients.text = '\n'.join(recipe['ingredients'])
        detail_screen.ids.recipe_directions.text = '\n'.join(recipe['directions'])
        detail_screen.ids.recipe_nutrition.text = '\n'.join(recipe['nutrition'])
        detail_screen.ids.recipe_prep_info.text = '\n'.join(recipe['prep_info'])
        self.current_recipe_url = recipe['url']
        self.switch_screen('recipe_detail')

    def open_recipe_link(self):
        if self.current_recipe_url:
            webbrowser.open(self.current_recipe_url)

    # def init_db(self):
    #     connection = sqlite3.connect('recipe.db')
    #     cursor = connection.cursor()
    #     cursor.execute('''
    #                   CREATE TABLE IF NOT EXISTS SAVED_RECIPES(
    #                   RECIPE_NAME VARCHAR(255),
    #                   RECIPE_URL VARCHAR(255),
    #                   RECIPE_INGREDIENTS TEXT,
    #                   RECIPE_DESCRIPTION TEXT,
    #                   RECIPE_DIRECTIONS TEXT,
    #                   RECIPE_NUTRITION TEXT,
    #                   RECIPE_PREP_INFO TEXT,
    #                   PRIMARY KEY (RECIPE_NAME)
    #                   );
    #                   ''')
    #     connection.commit()
    #     connection.close()

    def save_recipe(self, recipe):

        dbs.saved_recipes_db()
        connection = sqlite3.connect('/Users/shreyaskonanki/PycharmProjects/Wastefree/recipe.db')
        cursor = connection.cursor()

        # Convert list values to strings
        ingredients = ', '.join(recipe['ingredients'])  # Convert list to comma-separated string
        directions = '\n'.join(recipe['directions'])    # Convert list to newline-separated string
        nutrition = ', '.join(recipe['nutrition'])      # Convert list to comma-separated string
        prep_info = ', '.join(recipe['prep_info'])      # Convert list to comma-separated string

        # Insert the recipe into the database
        cursor.execute('''
        INSERT INTO SAVED_RECIPES (RECIPE_NAME, RECIPE_URL, RECIPE_INGREDIENTS, RECIPE_DESCRIPTION, RECIPE_DIRECTIONS,
        RECIPE_NUTRITION, RECIPE_PREP_INFO) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (recipe['name'], recipe['url'], ingredients, recipe['description'], directions, nutrition, prep_info))

        connection.commit()

        self.root.get_screen('recipe_list').ids.save_message.text = "Your recipe has been successfully saved"
        connection.close()

if __name__ == "__main__":
    RecipeApp().run()