import arcade
from arcade.gui import UIFlatButton, UILabel, UIManager, UIMessageBox


class Mywindow(arcade.Window):
    # THIS IS THE FUNCTION OF THE WINDOW
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(200, 200)
        arcade.set_background_color(arcade.color.TEA_ROSE)
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        # THIS IS GAME TITLE################################################################
        self.label = UILabel(
            x=50,
            y=800,
            text="BlackJack: The Game that made Satan Cry!!!",
            font_size=40,
            text_color=arcade.color.ORANGE,
        )
        self.ui_manager.add(self.label)

        ############# THIS IS THE PLAY BUTTON################################################################3
        self.play_button = self.make_button(
            x=500, y=250, text="Play Game", callback=self.message
        )
        self.ui_manager.add(self.play_button)

        ################# THIS IS THE QUIT BUTTON##############################################################3
        self.quit_button = self.make_button(
            x=600, y=400, text="Quit Game", callback=self.quit
        )
        self.ui_manager.add(self.quit_button)

        ############################ THIS IS THE MESSAGE BOX############################################################
        self.messagebox = UIMessageBox(
            width=70,
            height=120,
            message_text="Are you sure you wanna increase the DIFICULTY Little Boy????",
            title="Up DIFICULTY",
            buttons=("Yeah, Boomers Hit me, Rahhhhh!!!.",),
        )

    ######################################FUNCTION TO MAKE BUTTONS#############################################################
    def make_button(self, x, y, text, callback):
        button = UIFlatButton(
            width=50,
            height=25,
            text=text,
            x=x,
            y=y,
            interaction_buttons=(arcade.MOUSE_BUTTON_LEFT,),
        )
        button.on_click = callback
        return button

    #############THIS IS THE MESSAGE FUNCTION######################################
    def message(self, event):
        self.ui_manager.add(self.messagebox)

    #######THIS IS THE QUIT FUNCTION###############################################################
    def quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()


##########################LOADING THE GAME###############################################3
window = Mywindow(1200, 1050, "BlackJack")
arcade.run()
