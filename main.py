import arcade
from arcade.gui import UIFlatButton, UIManager


class Mywindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        arcade.set_background_color(arcade.color.TEA_ROSE)
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.play_button = UIFlatButton(
            width=50,
            height=25,
            text="Play",
            x=200,
            y=550,
            interaction_buttons=(arcade.MOUSE_BUTTON_LEFT),
        )
        self.play_button.on_click = print("Soon Man this shi is still in development.")

        """self.messagebox = UIMessageBox(
            width=70,
            height=120,
            message_text="Are you sure you wanna increase the DIFICULTY Little Boy????",
            title="Up DIFICULTY",
            buttons=("Yeah, Boomers Hit me, Rahhhhh!!!.",),
        )"""

        # self.ui_manager.add(self.messagebox)
        # self.ui_manager.add(self.game_title)
        self.ui_manager.add(self.play_button)

    def on_draw(self):
        self.clear()
        # arcade.draw_line(0, self.height, self.width, 0, arcade.color.AQUA, 3)
        # arcade.draw_point(550, 600, arcade.color.WHITE, 25)
        self.ui_manager.draw()
        arcade.draw_text(
            text="BlackJack: The Game that made Satan Cry!!!",
            x=50,
            y=800,
            font_size=40,
            color=arcade.color.ORANGE,
            align="center",
        )

    # def on_update(self):


window = Mywindow(1200, 1050, "BlackJack")
# text = MenuDialogBox()

arcade.run()
