import arcade
from arcade.gui import (
    UIFlatButton,
    UILabel,
    UIManager,
    UIMessageBox,
    UIOnActionEvent,
    UITextureButton,
)


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.background_texture = arcade.Sprite(
            "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/main menu.png"
        )
        self.background_list = arcade.SpriteList()
        scale_x = self.window.width / self.background_texture.width
        scale_y = self.window.height / self.background_texture.height
        self.background_texture.scale = max(scale_x, scale_y)
        self.background_texture.center_x = self.window.width // 2
        self.background_texture.center_y = self.window.height // 2

        self.background_list.append(self.background_texture)

        self.label = UILabel(
            x=50,
            y=800,
            text="BlackJack: The Game that made Satan Cry!!!",
            font_size=40,
            text_color=arcade.color.ORANGE,
        )
        self.ui_manager.add(self.label)

        self.play_button = self.make_button(
            340,
            470,
            200,
            75,
            self.show_message,
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/play.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/play_hovered.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/play_clicked.png"
            ),
        )
        self.ui_manager.add(self.play_button)

        self.rules_button = self.make_button(
            1450,
            460,
            200,
            75,
            self.show_rules,
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/rules_idle.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/rules_hover.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/rules_clicked.png"
            ),
        )
        self.ui_manager.add(self.rules_button)

        self.contact_button = self.make_button(
            320,
            160,
            180,
            75,
            self.show_contacts,
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/contact_idle.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/contact_hover.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/contact_clicked.png"
            ),
        )
        self.ui_manager.add(self.contact_button)

        self.quit_button = self.make_button(
            1450,
            130,
            200,
            75,
            lambda e: arcade.exit(),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/quit_idle.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/quit_hover.png"
            ),
            arcade.load_texture(
                "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/quit_clicked.png"
            ),
        )
        self.ui_manager.add(self.quit_button)

        self.messagebox = UIMessageBox(
            width=240,
            height=120,
            message_text="",
            title="Select Difficulty",
            buttons=("Beginner", "Experienced", "Expert"),
        )

        @self.messagebox.event("on_action")
        def on_action(event: UIOnActionEvent):
            # Remove the box from the UI
            self.ui_manager.remove(self.messagebox)

            if event.action == "Beginner":
                self.window.show_view(EasyMode())
            elif event.action == "Experienced":
                self.window.show_view(ModerateMode())
            elif event.action == "Expert":
                self.window.show_view(HardMode())

    def make_button(
        self,
        x,
        y,
        width,
        height,
        callback,
        texture,
        texture_hovered,
        texture_pressed,
    ):
        button = UITextureButton(
            width=width,
            height=height,
            x=x,
            y=y,
            texture=texture,
            texture_hovered=texture_hovered,
            texture_pressed=texture_pressed,
            interaction_buttons=(arcade.MOUSE_BUTTON_LEFT,),
        )
        button.on_click = callback
        return button

    def show_message(self, event):
        self.ui_manager.add(self.messagebox)

    def show_rules(self, event):
        self.window.show_view(RulesView())

    def show_contacts(self, event):
        self.window.show_view(ContactUs())

    def on_ui_event(self, event):
        if event.source == self.messagebox:
            if event.button.text == "Beginner":
                self.ui_manager.remove(self.messagebox)
                self.show_beginner(self)
            elif event.button.text == "Experienced":
                self.ui_manager.remove(self.messagebox)
                self.show_experienced(self)
            elif event.button.text == "Expert":
                self.ui_manager.remove(self.messagebox)
                self.show_expert(self)

    def show_beginner(self, event):
        self.window.show_view(EasyMode())

    def show_experienced(self, event):
        self.window.show_view(ModerateMode())

    def show_expert(self, event):
        self.window.show_view(HardMode())

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.ui_manager.draw()


class RulesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        self.rules_label = UILabel(
            x=50,
            y=700,
            text="The Rules are simple: You and the dealer each get 2 cards. Dealer shows one card. Try to beat dealer without going over 21.",
            font_size=20,
            text_color=arcade.color.TEAL,
            width=1800,
            multiline=True,
        )
        self.ui_manager.add(self.rules_label)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.back_to_menu
        self.ui_manager.add(back_button)

    def back_to_menu(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


class ContactUs(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        self.contact_us = UILabel(
            x=500,
            y=700,
            text="Prateek and Himesh",
            font_size=40,
            text_color=arcade.color.ALIZARIN_CRIMSON,
            multiline=True,
            bold=True,
        )

        self.ui_manager.add(self.contact_us)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_contact
        self.ui_manager.add(back_button)

    def menu_contact(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


#################EASY MODE##################################################


class EasyMode(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALIZARIN_CRIMSON)
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.background = arcade.Sprite(
            "/home/Prateek/Documents/Shi_I_Make/Projects/college_Project/Assets/Sprites/table.png"
        )
        self.easy_sprites = arcade.SpriteList()
        scale_x = self.window.width / self.background.width
        scale_y = self.window.height / self.background.height
        self.background.scale = max(scale_x, scale_y)
        self.background.center_x = self.window.width // 2
        self.background.center_y = self.window.height // 2

        self.easy_sprites.append(self.background)

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_easy
        self.ui_manager.add(back_button)

        self.messagebox = UIMessageBox(
            width=240,
            height=120,
            message_text="",
            title="Select Difficulty",
            buttons=("Beginner", "Experienced", "Expert"),
        )

        @self.messagebox.event("on_action")
        def on_action(event: UIOnActionEvent):
            # Remove the box from the UI
            self.ui_manager.remove(self.messagebox)

            if event.action == "Beginner":
                self.window.show_view(EasyMode())
            elif event.action == "Experienced":
                self.window.show_view(ModerateMode())
            elif event.action == "Expert":
                self.window.show_view(HardMode())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_messagebox(None)

    def show_messagebox(self, event):
        self.ui_manager.add(self.messagebox)

    def menu_easy(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.easy_sprites.draw()
        self.ui_manager.draw()


#################MODERATE MODE##################################################


class ModerateMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_moderate
        self.ui_manager.add(back_button)

    def menu_moderate(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


#################HARD MODE##################################################


class HardMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        back_button = UIFlatButton(
            x=500, y=100, width=150, height=40, text="Back to Menu"
        )
        back_button.on_click = self.menu_hard
        self.ui_manager.add(back_button)

    def menu_hard(self, event):
        self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


window = arcade.Window(1920, 1200, "BlackJack", center_window=True, enable_polling=True)
menu_view = MainMenu()
window.show_view(menu_view)
arcade.run()
