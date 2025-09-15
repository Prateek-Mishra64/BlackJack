import arcade
from arcade.gui import UIFlatButton, UILabel, UIManager, UIMessageBox


class Mywindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        arcade.set_background_color(arcade.color.TEA_ROSE)
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        self.label = UILabel(
            x=50,
            y=800,
            text="BlackJack: The Game that made Satan Cry!!!",
            font_size=40,
            text_color=arcade.color.ORANGE,
        )

        self.ui_manager.add(self.label)

        self.play_button = UIFlatButton(
            width=50,
            height=25,
            text="Play",
            x=200,
            y=550,
            interaction_buttons=(arcade.MOUSE_BUTTON_LEFT,),
        )
        self.ui_manager.add(self.play_button)

        self.play_button.on_click = self.message
        # self.ui_manager.add(self.message)

        self.messagebox = UIMessageBox(
            width=70,
            height=120,
            message_text="Are you sure you wanna increase the DIFICULTY Little Boy????",
            title="Up DIFICULTY",
            buttons=("Yeah, Boomers Hit me, Rahhhhh!!!.",),
        )

    def message(self, event):
        self.ui_manager.add(self.messagebox)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


window = Mywindow(1200, 1050, "BlackJack")
arcade.run()
