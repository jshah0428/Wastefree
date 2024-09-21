from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
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

KV = '''
ScreenManager:
    SearchScreen:
    RecipeListScreen:
    RecipeDetailScreen:

<SearchScreen>:
    name: 'search'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 10

        MDTopAppBar:
            title: "Recipe Search"
            elevation: 10

        MDTextField:
            id: search_field
            hint_text: "Enter ingredients..."
            mode: "rectangle"
            size_hint_x: None
            width: "300dp"
            pos_hint: {"center_x": .5}

        MDRaisedButton:
            text: "Search Recipes"
            pos_hint: {"center_x": .5}
            on_release: app.search_recipes()

<RecipeListScreen>:
    name: 'recipe_list'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Recipe List"
            left_action_items: [["arrow-left", lambda x: app.switch_screen('search')]]

        MDScrollView:
            MDList:
                id: recipe_list

<RecipeDetailScreen>:
    name: 'recipe_detail'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Recipe Details"
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
        self.theme_cls.theme_style = "Dark"
        self.current_recipe_url = None
        return Builder.load_string(KV)

    def switch_screen(self, screen_name):
        self.root.current = screen_name

    def search_recipes(self):
        search_text = self.root.get_screen('search').ids.search_field.text
        recipes = self.scraper(search_text)
        self.display_recipe_list(recipes)

    def display_recipe_list(self, recipes):
        recipe_list = self.root.get_screen('recipe_list').ids.recipe_list
        recipe_list.clear_widgets()
        for recipe in recipes:
            item = OneLineListItem(text=recipe['name'], on_release=lambda x, r=recipe: self.show_recipe_detail(r))
            recipe_list.add_widget(item)
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

    def display_recipe_list(self, recipes):
        recipe_list = self.root.get_screen('recipe_list').ids.recipe_list
        recipe_list.clear_widgets()

        for recipe in recipes:
            # Create a horizontal layout (BoxLayout) for each recipe item
            box_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height='48dp')

            # Create the recipe list item (OneLineListItem)
            item = OneLineListItem(text=recipe['name'], on_release=lambda x, r=recipe: self.show_recipe_detail(r))

            # Create the green "Save" button
            save_button = MDRaisedButton(
                text="Save",
                md_bg_color=[0, 1, 0, 1],  # Green background color (RGBA format)
                on_release=lambda x, r=recipe: self.save_recipe(r)  # Call save method when pressed
            )

            # Add the item and save button to the box layout
            box_layout.add_widget(item)
            box_layout.add_widget(save_button)

            # Add the box layout to the recipe list
            recipe_list.add_widget(box_layout)

        self.switch_screen('recipe_list')

    def init_db(self):
        connection = sqlite3.connect('recipe.db')
        cursor = connection.cursor()
        cursor.execute('''
                      CREATE TABLE IF NOT EXISTS SAVED_RECIPES(
                      RECIPE_NAME VARCHAR(255),
                      RECIPE_URL VARCHAR(255),
                      RECIPE_INGREDIENTS TEXT,
                      RECIPE_DESCRIPTION TEXT,
                      RECIPE_DIRECTIONS TEXT,
                      RECIPE_NUTRITION TEXT,
                      RECIPE_PREP_INFO TEXT,
                      PRIMARY KEY (RECIPE_NAME)
                      );
                      ''')
        connection.commit()
        connection.close()

    def save_recipe(self, recipe):
        self.init_db()

        connection = sqlite3.connect('recipe.db')
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
        connection.close()

if __name__ == "__main__":
    RecipeApp().run()