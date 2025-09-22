import arcade
from arcade.gui import UIFlatButton, UILabel, UIManager, UIMessageBox


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.TEA_ROSE)

        self.label = UILabel(
            x=50,
            y=800,
            text="BlackJack: The Game that made Satan Cry!!!",
            font_size=40,
            text_color=arcade.color.ORANGE,
        )
        self.ui_manager.add(self.label)

        self.play_button = self.make_button(
            500, 500, 100, 35, "Play Game", self.show_message
        )
        self.ui_manager.add(self.play_button)

        self.rules_button = self.make_button(
            500, 400, 100, 35, "Rules", self.show_rules
        )
        self.ui_manager.add(self.rules_button)

        self.contact_button = self.make_button(
            500, 300, 100, 35, "Contact Us", self.show_contacts
        )
        self.ui_manager.add(self.contact_button)

        self.quit_button = self.make_button(
            500, 200, 100, 35, "Quit Game", lambda e: arcade.exit()
        )
        self.ui_manager.add(self.quit_button)

        self.messagebox = UIMessageBox(
            width=240,
            height=120,
            message_text="",
            title="Select Difficulty",
            buttons=("Beginner", "Experienced", "Expert"),
        )

    def make_button(self, x, y, width, height, text, callback):
        button = UIFlatButton(
            width=width,
            height=height,
            x=x,
            y=y,
            text=text,
            interaction_buttons=(arcade.MOUSE_BUTTON_LEFT,),
        )
        button.on_click = callback
        return button

    def show_message(self, event):
        self.ui_manager.add(self.messagebox)

    def show_rules(self, event):
        self.window.show_view(RulesView())  # switch to rules view

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()

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


class EasyMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


class ModerateMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


class HardMode(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


window = arcade.Window(1920, 1050, "BlackJack")
menu_view = MainMenu()
window.show_view(menu_view)
arcade.run()
